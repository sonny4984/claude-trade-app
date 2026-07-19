/*
 * 「전문기관 연계 선도프로그램(사랑의 교실)」 교육결과 통보서를
 * 한글2020에서 바로 열리는 .docx 문서로 생성한다.
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

const FONT = "바탕";
const B = { style: BorderStyle.SINGLE, size: 6, color: "000000" };
// 24칸 × 400twip = 9600twip 폭 그리드 (칸 병합으로 열 폭을 조절)
const GRID = Array(24).fill(400);

function run(text, { bold = false, size = 22 } = {}) {
  return new TextRun({ text: String(text ?? ""), bold, size, font: FONT });
}

function para(text, { bold = false, size = 22, align = AlignmentType.CENTER, spacing } = {}) {
  return new Paragraph({ alignment: align, spacing, children: [run(text, { bold, size })] });
}

function cell(content, { span = 1, align = AlignmentType.CENTER, bold = false, size = 22 } = {}) {
  const children = Array.isArray(content) ? content : [para(content, { bold, size, align })];
  return new TableCell({ columnSpan: span, verticalAlign: VerticalAlign.CENTER, children });
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
    if (s) {
      sessionRows.push(
        row(
          [
            cell(s.date || "월      일", { span: 4 }),
            cell(s.content || "", { span: 14, align: AlignmentType.LEFT }),
            cell(s.hours || "", { span: 3 }),
            cell(d.counselor || "", { span: 3 }),
          ],
          480
        )
      );
    } else {
      sessionRows.push(
        row(
          [cell("월      일", { span: 4 }), cell("", { span: 14 }), cell("", { span: 3 }), cell("", { span: 3 })],
          480
        )
      );
    }
  }

  // 의견 셀: 본문 문단들 + 상담사 서명줄
  const opinionParas = String(d.opinion || "")
    .split(/\n+/)
    .filter((t) => t.trim())
    .map(
      (t) =>
        new Paragraph({
          alignment: AlignmentType.BOTH,
          spacing: { line: 340 },
          children: [run(" " + t.trim(), { size: 21 })],
        })
    );
  const opinionCellChildren = [
    ...(opinionParas.length ? opinionParas : [para("", {})]),
    para("", {}),
    para(`상담사    ${d.counselor || ""}      `, { align: AlignmentType.RIGHT, size: 22 }),
    para("", {}),
  ];

  const table = new Table({
    columnWidths: GRID,
    width: { size: 9600, type: WidthType.DXA },
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    borders: { top: B, bottom: B, left: B, right: B, insideHorizontal: B, insideVertical: B },
    rows: [
      row(
        [
          cell("수    신", { span: 4, bold: true }),
          cell(d.recipient, { span: 8 }),
          cell("관리번호", { span: 4, bold: true }),
          cell(d.docNo, { span: 8 }),
        ],
        520
      ),
      row([cell("인    적    사    항", { span: 24, bold: true })], 480),
      row(
        [
          cell("성    명", { span: 4, bold: true }),
          cell(d.name, { span: 4 }),
          cell("생년월일", { span: 4, bold: true }),
          cell(d.birth, { span: 4 }),
          cell("나    이", { span: 4, bold: true }),
          cell(d.age, { span: 4 }),
        ],
        520
      ),
      row(
        [
          cell("직    업", { span: 4, bold: true }),
          cell(d.job, { span: 8 }),
          cell("비행내용", { span: 4, bold: true }),
          cell(d.offense, { span: 8 }),
        ],
        520
      ),
      row([cell("교    육    내    용", { span: 24, bold: true })], 480),
      row(
        [
          cell("교육일자", { span: 4, bold: true }),
          cell("내용 및 결과", { span: 14, bold: true }),
          cell("운영시간", { span: 3, bold: true }),
          cell("강사명", { span: 3, bold: true }),
        ],
        460
      ),
      ...sessionRows,
      row([cell("종    합    의    견", { span: 24, bold: true })], 480),
      row(
        [
          cell("참여태도", { span: 4, bold: true }),
          cell(`적극(  ${mark("적극")}  ),      보통(  ${mark("보통")}  ),      소극(  ${mark("소극")}  )`, {
            span: 20,
            align: AlignmentType.LEFT,
          }),
        ],
        520
      ),
      row(
        [
          cell("의    견", { span: 4, bold: true }),
          new TableCell({ columnSpan: 20, verticalAlign: VerticalAlign.CENTER, children: opinionCellChildren }),
        ],
        4200
      ),
      row([cell(d.issueDate, { span: 24, size: 26 })], 620),
      row([cell(d.org, { span: 24, bold: true, size: 30 })], 720),
    ],
  });

  return new Document({
    styles: { default: { document: { run: { font: FONT, size: 22 } } } },
    sections: [
      {
        properties: {
          page: {
            margin: { top: 900, bottom: 900, left: 1153, right: 1153 },
          },
        },
        children: [
          para("「전문기관 연계 선도프로그램(사랑의 교실)」 교육결과 통보서", {
            bold: true,
            size: 30,
            spacing: { after: 240 },
          }),
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
