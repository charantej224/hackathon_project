from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch



def get_answer_for_question(question, context):
    """
    Name: get_answer_for_question
    :param question,content
    :return summary String.
    """
    # Load the fine-tuned model
    tokenizer = AutoTokenizer.from_pretrained("/home/sivakumar/BERT_FineTuning_Wiki/models_questions/bert")
    model = AutoModelForQuestionAnswering.from_pretrained("/home/sivakumar/BERT_FineTuning_Wiki/models_questions/bert")
    # 1. TOKENIZE THE INPUT
    # note: if you don't include return_tensors='pt' you'll get a list of lists which is easier for
    # exploration but you cannot feed that into a model.
    inputs = tokenizer.encode_plus(question, context, return_tensors="pt")

    # 2. OBTAIN MODEL SCORES
    # the AutoModelForQuestionAnswering class includes a span predictor on top of the model.
    # the model returns answer start and end scores for each word in the text
    answer_start_scores, answer_end_scores = model(**inputs)
    answer_start = torch.argmax(
        answer_start_scores)  # get the most likely beginning of answer with the argmax of the score
    answer_end = torch.argmax(answer_end_scores) + 1  # get the most likely end of answer with the argmax of the score

    # 3. GET THE ANSWER SPAN
    # once we have the most likely start and end tokens, we grab all the tokens between them
    # and convert tokens back to words!
    result = tokenizer.convert_tokens_to_string(
        tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end]))
    return  result



# question = "Who ruled Macedonia"
#
# context = """Macedonia was an ancient kingdom on the periphery of Archaic and Classical Greece,
# and later the dominant state of Hellenistic Greece. The kingdom was founded and initially ruled
# by the Argead dynasty, followed by the Antipatrid and Antigonid dynasties. Home to the ancient
# Macedonians, it originated on the northeastern part of the Greek peninsula. Before the 4th
# century BC, it was a small kingdom outside of the area dominated by the city-states of Athens,
# Sparta and Thebes, and briefly subordinate to Achaemenid Persia."""

# answer = get_answer_for_question(question, context)
# print(answer)




