File Structure:

.
├── ui/
│   └── index.html
├── app/
│   ├── tasks/
│   │   └── indexing.py
│   ├── utils/
│   │   └── logger.py
│   ├── agent/
│   │   ├── planner.py
│   │   ├── controller.py
│   │   └── tools.py
│   ├── rag/
│   │   ├── chunker.py
│   │   ├── context_builder.py
│   │   ├── retriever.py
│   │   ├── vectorstore.py
│   │   ├── llm.py
│   │   ├── embeddings.py
│   │   ├── loader.py
│   │   ├── answer_generator.py
│   │   └── prompt.py
│   ├── data/
│   │   └── vectorstore/
│   │       └── chroma.sqlite3
│   ├── config.py
│   └── main.py
├── data/
│   ├── docs/
│   │   ├── “PARIVAAR” - Employee and Employee Family Assistance.pdf
│   │   ├── Leave Policy.pdf
│   │   ├── Cabin Policy.pdf
│   │   ├── Employee Personal Loan Policy.pdf
│   │   ├── Domestic Travel Policy.pdf
│   │   └── Clean Desk Policy.pdf
│   └── vectorstore/
│       ├── c125b5d9-cd4b-4f22-8364-c4490d99d897/
│       │   ├── data_level0.bin
│       │   ├── length.bin
│       │   ├── link_lists.bin
│       │   ├── header.bin
│       │   └── index_metadata.pickle
│       └── chroma.sqlite3
├── .env
├── requirements.txt
├── run.sh
├── test_rag.py
└── run_indexing.py
