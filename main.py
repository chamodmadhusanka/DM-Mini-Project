import gradio as gr
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200, "scheme": "http"}])


def match_query(field, value):
    query = {
        "query": {
            "match": {
                field: value
            }
        },
        "size": 1000
    }
    result = es.search(index="poem", body=query)
    return result


def format_poem_response(poem_data):
    response_string = ""
    for obj in poem_data:
        cleaned_data = {key: value.replace('\n', '') if isinstance(value, str) else value for key, value in
                        obj["_source"].items()}
        response_string += '\n'.join([f'{key}: {value}' for key, value in cleaned_data.items()])
        response_string += "\n \n"
    return response_string


def custom_response_handler(key, data):
    keyword = "poem_name"
    key_to_keyword = {
        "Poem Name": "poem_name",
        "Poet": "poet",
        "Line": "line",
        "Metaphorical Term": "metaphorical_terms"
    }

    keyword = key_to_keyword.get(key, "poem_name")

    print(keyword, data)
    search_result = match_query(keyword, data)
    return format_poem_response((search_result["hits"])["hits"])


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # Metaphorica - Poem Search Application

        """)
    input_1 = gr.Radio(["Poem Name", "Poet", "Line", "Metaphorical Term"], label="Select input field of the poem")
    input_2 = gr.Textbox(lines=2, label="Enter the word or phrase")
    btn = gr.Button(value="Search")
    output = gr.Textbox(value="", label="Result")

    btn.click(fn=custom_response_handler,
              inputs=[
                  input_1,
                  input_2
              ], outputs=[output], )

demo.launch()

