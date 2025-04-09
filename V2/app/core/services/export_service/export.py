class ExportService:
    def export(self, entity, export_format: str) -> str:
        if export_format == "pdf":
            return self._export_to_pdf(entity)
        elif export_format == "csv":
            return self._export_to_csv(entity)
        elif export_format == "excel":
            return self._export_to_excel(entity)
        else:
            raise ValueError(f"Unsupported export export_format: {export_format}")

    def _export_to_pdf(self, entity) -> str:
        # generate PDF file
        # Return file path
        ...

    def _export_to_csv(self, entity) -> str:
        # generate CSV file
        ...

    def _export_to_excel(self, entity) -> str:
        # generate Excel file
        ...
