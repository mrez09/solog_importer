from datetime import date, datetime, time, timedelta
from typing import Literal

from pydantic import BaseModel, Field, model_validator

FormulaAttribute = str | int | float | bool | None
CellValue = (
    str
    | int
    | float
    | bool
    | date
    | datetime
    | time
    | timedelta
    | dict[str, FormulaAttribute]
    | None
)


class WorkbookRecord(BaseModel):
    source_file_id: str = Field(pattern=r"^[a-f0-9]{32}$")
    source_filename: str
    storage_filename: str = Field(pattern=r"^[a-f0-9]{32}\.xlsx$")
    source_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    size_bytes: int = Field(gt=0)
    uploaded_at: datetime
    read_status: Literal["readable", "error"]
    read_error: str | None = None

    @model_validator(mode="after")
    def storage_name_matches_source_id(self) -> "WorkbookRecord":
        if self.storage_filename != f"{self.source_file_id}.xlsx":
            raise ValueError("Nama penyimpanan harus sesuai dengan identitas file.")
        return self


class UploadResult(BaseModel):
    status: Literal["accepted", "rejected"]
    source_filename: str
    workbook: WorkbookRecord | None = None
    error: str | None = None


class SourceLocator(BaseModel):
    source_file_id: str
    source_filename: str
    source_sha256: str
    sheet_name: str
    sheet_index: int
    row_number: int
    cell_coordinate: str | None = None


class CellStyleInfo(BaseModel):
    style_id: int
    font_name: str | None = None
    font_size: float | None = None
    font_bold: bool = False
    font_italic: bool = False
    font_color: str | None = None
    fill_type: str | None = None
    fill_color: str | None = None
    horizontal_alignment: str | None = None
    vertical_alignment: str | None = None
    wrap_text: bool = False
    border_sides: list[str]


class CellInfo(BaseModel):
    coordinate: str
    row_number: int
    column_number: int
    value: CellValue
    data_type: str
    formula: str | None = None
    formula_metadata: dict[str, FormulaAttribute] | None = None
    number_format: str
    style: CellStyleInfo
    is_empty: bool
    source_locator: SourceLocator


class MergedRangeInfo(BaseModel):
    coordinate: str
    main_cell_coordinate: str
    member_coordinates: list[str]


class WorksheetInfo(BaseModel):
    name: str
    sheet_index: int
    status: Literal["visible", "hidden", "veryHidden"]
    max_row: int
    max_column: int
    dimensions: str
    preview_cells: list[CellInfo]
    merged_ranges: list[MergedRangeInfo]


class WorksheetPage(BaseModel):
    name: str
    sheet_index: int
    max_row: int
    max_column: int
    cells: list[CellInfo]


class WorkbookDetail(BaseModel):
    source: WorkbookRecord
    worksheet_names: list[str]
    worksheets: list[WorksheetInfo]


class WorkbookList(BaseModel):
    workbooks: list[WorkbookRecord]


class UploadBatchResult(BaseModel):
    results: list[UploadResult]
    workbooks: list[WorkbookRecord]
