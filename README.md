# Alina un personaje Real


# Flow
''' mermaid
flowchart TD
    Us[Usuario] -->|User enters Prompt|Un(Unity)
    Un --> R{Rag}
    R <--> |Query para Contexto|C(ChromaDB)
    R --> |Contexto+Prompt|O(Ollama)
    O --> |Respuesta del LLM|R
    R --> |Respuesta del LLMU editada|Un
    Un --> |Usuario lee y escucha respuesta|Us
'''
