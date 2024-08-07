import gradio as gr
from api.modules.graph import GraphApp


def create_label(items, default):
    return items[0]["Value"] if items[0]["Value"] != "" else default


def handle_text_only_chat(node, input_elements, model: GraphApp):
    label = create_label(node["Items"], "Chat")
    rtl = node["Items"][2]["Value"]
    placeholder = node["Items"][1]["Value"]
    likeable = node["Items"][3]["Value"]

    textbox = gr.Textbox(placeholder=placeholder, rtl=rtl, elem_id="chat_texbox")
    return gr.ChatInterface(
        fn=model.execute_chat,
        multimodal=False,
        fill_height=True,
        additional_inputs=input_elements,
        chatbot=gr.Chatbot(
            label=label, rtl=rtl, likeable=likeable, elem_id="chat_chatbot"
        ),
        textbox=textbox,
    )


def handle_multimodal_chat(node, input_elements, model: GraphApp):
    label = create_label(node["Items"], "Chat")
    rtl = node["Items"][2]["Value"]
    placeholder = node["Items"][1]["Value"]
    likeable = node["Items"][3]["Value"]

    textbox = gr.MultimodalTextbox(
        placeholder=placeholder, rtl=rtl, elem_id="chat_multimodal"
    )
    return gr.ChatInterface(
        fn=model.execute_chat,
        multimodal=True,
        fill_height=True,
        additional_inputs=input_elements,
        chatbot=gr.Chatbot(
            label=label, rtl=rtl, likeable=likeable, elem_id="chat_chatbot"
        ),
        textbox=textbox,
    )


def handle_text_input(node):
    label = create_label(node["Items"], "Textbox")
    return gr.Textbox(
        label=label,
        placeholder=node["Items"][1]["Value"],
        type=node["Items"][2]["Value"],
        elem_id=node["Id"],
    )


def handle_image_input(node):
    label = create_label(node["Items"], "Image")
    return gr.Image(label=label, elem_id=node["Id"])


def handle_audio_input(node):
    label = create_label(node["Items"], "Audio")
    return gr.Audio(label=label, elem_id=node["Id"])


def handle_video_input(node):
    label = create_label(node["Items"], "Video")
    return gr.Video(label=label, elem_id=node["Id"])


def handle_file_input(node):
    label = create_label(node["Items"], "File")
    return gr.File(label=label, elem_id=node["Id"])


def handle_text_output(node):
    label = create_label(node["Items"], "Result")
    return gr.Textbox(
        label=label,
        placeholder=node["Items"][1]["Value"],
        interactive=False,
        elem_id=node["Id"],
    )


def handle_llm(node):
    return gr.Textbox(visible=False, elem_id=node["Id"])


def handle_system_prompt(node):
    return gr.Textbox(visible=False, elem_id=node["Id"])


dispatch = {
    "Text-Only Chat": handle_text_only_chat,
    "Multimodal Chat": handle_multimodal_chat,
    "Text Input": handle_text_input,
    "Image Input": handle_image_input,
    "Audio Input": handle_audio_input,
    "Video Input": handle_video_input,
    "File Input": handle_file_input,
    "Text Output": handle_text_output,
    "LLM": handle_llm,
    "System Prompt": handle_system_prompt,
}
