import re

from flask import Flask, jsonify, request

app = Flask(__name__)


def get_sentence(lines, line_no, start, end, key):
    starting_sentence = "".join(lines[:line_no - 1]) + lines[line_no][:start]

    ending_sentence = lines[line_no][end:] + "".join(lines[line_no + 1:])
    starting_sentence = starting_sentence[starting_sentence.rfind('.') + 1:]
    ending_sentence = ending_sentence[:ending_sentence.find('.')]
    return (starting_sentence + key + ending_sentence).replace("\n", "")


def get_occurance(key):
    result = []
    with open('king-i.txt') as f:
        lines = f.readlines()
    for i in range(len(lines)):
        matches = list(re.finditer(key.lower(), lines[i].lower()))
        for match in matches:
            in_sentence = get_sentence(lines, i, match.start(), match.end(), key)
            result.append(
                {"start:": match.start() + 1, "end": match.end() + 1, "line": i + 1, "in_sentence": in_sentence})

    return result


@app.route("/search")
def search():
    key = request.args.get('key')
    occurrences = get_occurance(key)
    data = {
        "query_text": key,
        "number_of_occurrences": len(occurrences),
        "occurrences": occurrences
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run()
