"""
pdf_report.py

Provee la clase PDFReportGenerator (a modo de method object) para la generación del reporte correspondiente
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple
import pandas as pd
from fpdf import FPDF

@dataclass
class ReportStyle:
    title_font: Tuple[str, int, str] = ("Arial", 12, 'B')
    header_font: Tuple[str, int, str] = ("Arial", 11, 'B')
    body_font: Tuple[str, int] = ("Arial", 10)
    line_spacing: int = 6
    page_margins: int = 10

from src.constants import REPORT_DIR

class PDFReportGenerator:
    def __init__(self, output_dir: str = REPORT_DIR, style: ReportStyle = None):
        self.output_dir = Path(output_dir)
        self.style = style or ReportStyle()

    def generate(self, df: pd.DataFrame, filename: str = 'report.pdf') -> str:
        """Método principal"""
        output_path = self.output_dir / filename

        try:
            pdf = FPDF()
            pdf.add_page()
            self._add_title(pdf)
            self._add_candidates(pdf, df)
            pdf.output(output_path)
            return str(output_path.absolute())

        except Exception as e:
            raise RuntimeError(f"Report generation failed with Error: {str(e)}") from e

    def _add_title(self, pdf: FPDF):
        font, size, style = self.style.title_font
        pdf.set_font(font, style=style, size=size)
        pdf.cell(0, 10, "Reporte de Candidatos Preseleccionados", ln=True, align='C')
        pdf.ln(self.style.line_spacing)

    def _add_candidates(self, pdf: FPDF, df: pd.DataFrame):
        for _, row in df.iterrows():
            self._add_candidate_header(pdf, row)
            self._add_candidate_details(pdf, row)
            pdf.ln(self.style.line_spacing)

    def _add_candidate_header(self, pdf: FPDF, row):
        font, size, style = self.style.header_font
        pdf.set_font(font, style=style, size=size)
        pdf.cell(0, 8, f"{row['full_name']} - {row['degree']} student", ln=True)

    def _add_candidate_details(self, pdf: FPDF, row):
        font, size = self.style.body_font
        pdf.set_font(font, size=size)

        details = [
            f"{row['college']} - Academic average: ({row['academic_average']:.2f})",
            f"Skills: {self._format_skills(row['skills'])}",
            f"Preselection score: {row['score']:.1f}",
            f"Email: {row['email']}",
        ]

        for detail in details:
            pdf.cell(0, 6, detail, ln=True)

    @staticmethod
    def _format_skills(skills):
        return ', '.join(skills)
        # fix debido al refactor de CandidateService!
        #if pd.notna(skills):
        #    return ', '.join(skills.split(','))
        #return ''