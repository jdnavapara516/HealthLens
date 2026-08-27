from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentChunker:
    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 150,
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

    def split_pages(self, pages: list[dict]) -> list[dict]:
        print("Splitting pages into chunks...")
        chunks = []

        for page in pages:
            page_number = page["page"]
            content = page["content"]

            page_chunks = self.splitter.split_text(content)

            for chunk in page_chunks:
                chunks.append(
                    {
                        "content": chunk,
                        "page": page_number,
                    }
                )

        return chunks
