/*
 * 「전문기관 연계 선도프로그램(사랑의 교실)」 교육결과 통보서를
 * 한글2020에서 바로 열리는 .docx 문서로 생성한다.
 * 실제 통보서 출력물 사진과 칸 비율·글꼴·배치를 맞춘 레이아웃.
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

const FONT = "굴림";
const B = { style: BorderStyle.SINGLE, size: 6, color: "000000" };
// 48칸 × 200twip = 9600twip 폭 그리드 (칸 병합으로 열 폭을 조절)
const GRID = Array(48).fill(200);

function run(text, { bold = false, size = 22 } = {}) {
  return new TextRun({ text: String(text ?? ""), bold, size, font: FONT });
}

function para(text, { bold = false, size = 22, align = AlignmentType.CENTER, spacing } = {}) {
  return new Paragraph({ alignment: align, spacing, children: [run(text, { bold, size })] });
}

function cell(content, { span = 1, align = AlignmentType.CENTER, bold = false, size = 22, vAlign = VerticalAlign.CENTER } = {}) {
  const children = Array.isArray(content) ? content : [para(content, { bold, size, align })];
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
  const mark = (v) => (p === v ? "✔" : "    ");

  // 교육내용 5줄: 채워진 회차 + 빈 줄
  const sessionRows = [];
  for (let i = 0; i < Math.max(5, sessions.length); i++) {
    const s = sessions[i];
    sessionRows.push(
      row(
        [
          cell(s?.date || "월      일", { span: 6 }),
          cell(s?.content || "", { span: 31, align: s ? AlignmentType.LEFT : AlignmentType.CENTER }),
          cell(s?.hours || "", { span: 6 }),
          cell(s ? d.counselor || "" : "", { span: 5 }),
        ],
        480
      )
    );
  }

  // 의견 셀: 본문 문단들 + 상담사 서명줄 (이름은 한 글자씩 띄어 씀)
  const spacedName = String(d.counselor || "").replace(/\s+/g, "").split("").join(" ");
  const opinionParas = String(d.opinion || "")
    .split(/\n+/)
    .filter((t) => t.trim())
    .map(
      (t) =>
        new Paragraph({
          alignment: AlignmentType.BOTH,
          spacing: { line: 360 },
          children: [run("  " + t.trim(), { size: 21 })],
        })
    );
  const opinionCellChildren = [
    ...(opinionParas.length ? opinionParas : [para("", {})]),
    para("", {}),
    para(`상담사    ${spacedName}        `, { align: AlignmentType.RIGHT, size: 24 }),
  ];

  const table = new Table({
    columnWidths: GRID,
    width: { size: 9600, type: WidthType.DXA },
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    borders: { top: B, bottom: B, left: B, right: B, insideHorizontal: B, insideVertical: B },
    rows: [
      row(
        [
          cell("수    신", { span: 6, bold: true }),
          cell(d.recipient, { span: 19 }),
          cell("관리번호", { span: 8, bold: true }),
          cell(d.docNo, { span: 15 }),
        ],
        520
      ),
      row([cell("인    적    사    항", { span: 48, bold: true })], 500),
      row(
        [
          cell("성    명", { span: 6, bold: true }),
          cell(d.name, { span: 11 }),
          cell("생년월일", { span: 8, bold: true }),
          cell(d.birth, { span: 8 }),
          cell("나    이", { span: 6, bold: true }),
          cell(d.age, { span: 9 }),
        ],
        520
      ),
      row(
        [
          cell("직    업", { span: 6, bold: true }),
          cell(d.job, { span: 19 }),
          cell("비행내용", { span: 8, bold: true }),
          cell(d.offense, { span: 15 }),
        ],
        520
      ),
      row([cell("교    육    내    용", { span: 48, bold: true })], 500),
      row(
        [
          cell("교육일자", { span: 6, bold: true }),
          cell("내용 및 결과", { span: 31, bold: true }),
          cell("운영시간", { span: 6, bold: true }),
          cell("강사명", { span: 5, bold: true }),
        ],
        460
      ),
      ...sessionRows,
      row([cell("종    합    의    견", { span: 48, bold: true })], 500),
      row(
        [
          cell("참여태도", { span: 6, bold: true }),
          cell(` 적극(  ${mark("적극")}  ),    보통(  ${mark("보통")}  ),    소극(  ${mark("소극")}  )`, {
            span: 42,
            align: AlignmentType.LEFT,
          }),
        ],
        520
      ),
      row(
        [
          cell("의    견", { span: 6, bold: true }),
          new TableCell({ columnSpan: 42, verticalAlign: VerticalAlign.TOP, children: opinionCellChildren }),
        ],
        5400
      ),
    ],
  });

  return new Document({
    styles: { default: { document: { run: { font: FONT, size: 22 } } } },
    sections: [
      {
        properties: {
          page: {
            margin: { top: 900, bottom: 700, left: 1153, right: 1153 },
          },
        },
        children: [
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { after: 300 },
            children: [
              new TextRun({
                text: "「전문기관 연계 선도프로그램(사랑의 교실)」교육결과 통보서",
                bold: true,
                size: 32,
                font: FONT,
                underline: {},
              }),
            ],
          }),
          table,
          // 사진과 동일하게 날짜·기관장 명의는 표 밖(테두리 없음)에 크게
          para(d.issueDate, { size: 26, spacing: { before: 400 } }),
          para(d.org, { bold: true, size: 36, spacing: { before: 200 } }),
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
