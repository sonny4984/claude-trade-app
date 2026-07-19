/*
 * 「전문기관 연계 선도프로그램(사랑의 교실)」 교육결과 통보서를
 * 한글2020에서 바로 열리는 .docx 문서로 생성한다.
 *
 * 레이아웃은 원본 HWPX에서 추출한 실측값을 그대로 사용한다.
 *  - 페이지: A4, 여백 상하좌우 1134twip
 *  - 본표: 10열 그리드(열 폭 twip) [1215,2233,1385,170,1353,468,569,427,678,1105] = 9603
 *  - 테두리: 바깥 0.4mm(size9), 안쪽 0.12mm(size3)
 *  - 글꼴: 본문 한양그래픽 12pt, 구분행 13pt 진하게, 제목 HY헤드라인M 17pt(하단 이중선)
 *  - 하단 행: 날짜 14pt / 기관명 16pt 진하게 (표 마지막 행 안)
 *
 * 직인(도장)은 문서에 넣지 않는다 — 출력 후 기존 방식대로 날인한다.
 */
import {
  Document,
  Packer,
  Paragraph,
  TextRun,
  Table,
  TableRow,
  TableCell,
  WidthType,
  AlignmentType,
  VerticalAlign,
  BorderStyle,
  HeightRule,
} from "docx";

const MAIN_FONT = "한양그래픽";
const TITLE_FONT = "HY헤드라인M";
// 원본 10열 그리드 (twip)
const GRID = [1215, 2233, 1385, 170, 1353, 468, 569, 427, 678, 1105];
const TBL_W = 9603;
const OUTER = { style: BorderStyle.SINGLE, size: 9, color: "000000" }; // 0.4mm
const INNER = { style: BorderStyle.SINGLE, size: 3, color: "000000" }; // 0.12mm
const NONE = { style: BorderStyle.NONE, size: 0, color: "auto" };

function run(text, { bold = false, size = 24, font = MAIN_FONT } = {}) {
  return new TextRun({ text: String(text ?? ""), bold, size, font });
}

function para(text, { bold = false, size = 24, align = AlignmentType.CENTER, line, font } = {}) {
  return new Paragraph({
    alignment: align,
    spacing: line ? { line } : undefined,
    children: [run(text, { bold, size, font })],
  });
}

function cell(content, { span = 1, align = AlignmentType.CENTER, bold = false, size = 24, line, vAlign = VerticalAlign.CENTER } = {}) {
  const children = Array.isArray(content) ? content : [para(content, { bold, size, align, line })];
  return new TableCell({ columnSpan: span, verticalAlign: vAlign, children });
}

function row(cells, minHeight) {
  return new TableRow({
    children: cells,
    height: minHeight ? { value: minHeight, rule: HeightRule.ATLEAST } : undefined,
  });
}

/**
 * data: { recipient, docNo, name, birth, age, job, offense,
 *         sessions: [{date, content, hours}], participation, opinion,
 *         counselor, issueDate, org }
 */
export function buildReportDoc(data) {
  const d = data || {};
  const sessions = Array.isArray(d.sessions) ? d.sessions.filter((s) => s && (s.date || s.content)) : [];
  const p = d.participation || "적극";
  // 원본 표기: 체크는 "(  ✔  )", 빈 칸은 자리마다 공백 수가 다름
  const slot = (v, blank) => (p === v ? "(  ✔  )" : `(${blank})`);

  // 교육내용 5줄: 채워진 회차 + 빈 줄 (원본과 동일하게 최소 5줄)
  const sessionRows = [];
  for (let i = 0; i < Math.max(5, sessions.length); i++) {
    const s = sessions[i];
    sessionRows.push(
      row(
        [
          cell(s ? " " + (s.date || "") : "   월  일", { span: 1, align: AlignmentType.LEFT }),
          cell(s ? " " + (s.content || "") : " ", { span: 6, align: AlignmentType.LEFT }),
          cell(s?.hours || "", { span: 2 }),
          cell(s ? d.counselor || "" : "", { span: 1 }),
        ],
        466
      )
    );
  }

  // 의견 셀: 원본 구조 그대로 — 빈 줄, 본문(양쪽정렬 160%), 공백으로 자리 잡은 서명줄
  const spacedName = String(d.counselor || "").replace(/\s+/g, "").split("").join(" ");
  const opinionParas = String(d.opinion || "")
    .split(/\n+/)
    .filter((t) => t.trim())
    .map(
      (t) =>
        new Paragraph({
          alignment: AlignmentType.BOTH,
          spacing: { line: 384 },
          children: [run(" " + t.trim() + " ", { size: 24 })],
        })
    );
  const opinionCellChildren = [
    para(" ", { align: AlignmentType.LEFT, line: 384 }),
    ...opinionParas,
    para(`                       상담사   ${spacedName}  `, { align: AlignmentType.LEFT, size: 24, line: 384 }),
  ];

  // 제목: 원본은 1×1 표(테두리 없음, 하단만 이중선)
  const titleTable = new Table({
    columnWidths: [9276],
    width: { size: 9276, type: WidthType.DXA },
    alignment: AlignmentType.CENTER,
    margins: { top: 28, bottom: 28, left: 28, right: 28 },
    borders: {
      top: NONE,
      left: NONE,
      right: NONE,
      bottom: { style: BorderStyle.DOUBLE, size: 6, color: "000000" },
      insideHorizontal: NONE,
      insideVertical: NONE,
    },
    rows: [
      row(
        [
          new TableCell({
            verticalAlign: VerticalAlign.CENTER,
            children: [
              new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [
                  new TextRun({
                    text: "｢전문기관 연계 선도프로그램(사랑의 교실)｣교육결과 통보서",
                    size: 34,
                    font: TITLE_FONT,
                    characterSpacing: -7,
                  }),
                ],
              }),
            ],
          }),
        ],
        589
      ),
    ],
  });

  const table = new Table({
    columnWidths: GRID,
    width: { size: TBL_W, type: WidthType.DXA },
    margins: { top: 28, bottom: 28, left: 28, right: 28 },
    borders: { top: OUTER, bottom: OUTER, left: OUTER, right: OUTER, insideHorizontal: INNER, insideVertical: INNER },
    rows: [
      row(
        [
          cell("수  신", { span: 1 }),
          cell(d.recipient, { span: 3 }),
          cell("관리번호", { span: 2 }),
          cell(d.docNo, { span: 4 }),
        ],
        522
      ),
      row([cell("인   적   사   항", { span: 10, bold: true, size: 26 })], 542),
      row(
        [
          cell("성  명", { span: 1 }),
          cell(d.name, { span: 1 }),
          cell("생년월일", { span: 1 }),
          cell(d.birth, { span: 2 }),
          cell("나이", { span: 3 }),
          cell(d.age, { span: 2 }),
        ],
        409
      ),
      row(
        [
          cell("직  업", { span: 1 }),
          cell(d.job, { span: 4 }),
          cell("비행내용", { span: 3 }),
          cell(d.offense, { span: 2 }),
        ],
        409
      ),
      row([cell("교   육  내  용", { span: 10, bold: true, size: 26 })], 486),
      row(
        [
          cell("교육일자", { span: 1 }),
          cell("내용 및 결과", { span: 6 }),
          cell("운영시간", { span: 2 }),
          cell("강사명", { span: 1 }),
        ],
        466
      ),
      ...sessionRows,
      row([cell("종   합   의   견", { span: 10, bold: true, size: 26 })], 486),
      row(
        [
          cell("참여태도", { span: 1 }),
          cell(`  적극${slot("적극", "     ")},  보통${slot("보통", "   ")},  소극${slot("소극", "     ")}`, {
            span: 9,
            align: AlignmentType.LEFT,
          }),
        ],
        502
      ),
      row(
        [
          cell("의견", { span: 1 }),
          new TableCell({ columnSpan: 9, verticalAlign: VerticalAlign.TOP, children: opinionCellChildren }),
        ],
        4880
      ),
      row(
        [
          cell(
            [
              para(d.issueDate, { size: 28, line: 384 }),
              para((d.org || "") + " ", { bold: true, size: 32, line: 360 }),
            ],
            { span: 10 }
          ),
        ],
        1090
      ),
    ],
  });

  return new Document({
    styles: { default: { document: { run: { font: MAIN_FONT, size: 24 } } } },
    sections: [
      {
        properties: {
          page: {
            margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 },
          },
        },
        children: [
          titleTable,
          new Paragraph({ spacing: { before: 60, after: 60 }, children: [new TextRun({ text: "", size: 8 })] }),
          table,
        ],
      },
    ],
  });
}

/** 브라우저에서 .docx 파일로 내려받기 */
export async function downloadReportDocx(data) {
  const blob = await Packer.toBlob(buildReportDoc(data));
  const safe = (s) => String(s || "").replace(/[\\/:*?"<>|\s]+/g, "_");
  const fname = `결과통보서_${safe(data.name) || "이름"}_${safe(data.docNo) || "번호"}.docx`;
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = fname;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 4000);
  return fname;
}
