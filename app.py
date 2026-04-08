from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage
ideas = []
idea_id = 1

# Create idea
@app.route('/ideas', methods=['POST'])
def create_idea():
    global idea_id
    data = request.json

    idea = {
        "id": idea_id,
        "title": data.get("title"),
        "description": data.get("description"),
        "votes": 0
    }

    ideas.append(idea)
    idea_id += 1

    return jsonify(idea)

# Get all ideas (sorted by votes)
@app.route('/ideas', methods=['GET'])
def get_ideas():
    return jsonify(sorted(ideas, key=lambda x: x["votes"], reverse=True))

# Vote
@app.route('/ideas/<int:id>/vote', methods=['POST'])
def vote_idea(id):
    data = request.json
    vote_type = data.get("vote")  # "up" or "down"

    for idea in ideas:
        if idea["id"] == id:
            if vote_type == "up":
                idea["votes"] += 1
            elif vote_type == "down":
                idea["votes"] -= 1
            return jsonify(idea)

    return jsonify({"error": "Idea not found"}), 404

# "AI Improve" (mock version)
@app.route('/ideas/<int:id>/improve', methods=['POST'])
def improve_idea(id):
    for idea in ideas:
        if idea["id"] == id:
            idea["description"] = idea["description"] + " (Enhanced with AI 🚀)"
            return jsonify(idea)

    return jsonify({"error": "Idea not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)

