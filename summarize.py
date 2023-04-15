from transformers import pipeline


def summarize_text(text_input):
	summarizer = pipeline("summarization")
	return summarizer(text_input)[0]['summary_text']
