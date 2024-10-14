from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for children, chores, rewards
children = {
    "child_id_1": {"name": "Child One", "balance": 100, "chores": [], "rewards": []}
}
chores_db = []
rewards_db = []

@app.route('/add_chore', methods=['POST'])
def add_chore():
    data = request.json
    chore = {
        'id': len(chores_db) + 1,
        'name': data['name'],
        'description': data['description'],
        'recurrence': data['recurrence'],
        'custom_recurrence_days': data['custom_recurrence_days'],
        'reward_amount': data['reward_amount'],
    }
    chores_db.append(chore)
    return jsonify({'message': 'Chore added successfully'}), 200

@app.route('/add_reward', methods=['POST'])
def add_reward():
    data = request.json
    reward = {
        'id': len(rewards_db) + 1,
        'name': data['name'],
        'cost': data['cost']
    }
    rewards_db.append(reward)
    return jsonify({'message': 'Reward added successfully'}), 200

@app.route('/complete_chore', methods=['POST'])
def complete_chore():
    data = request.json
    child_id = data['child_id']
    chore_id = data['chore_id']
    child = children.get(child_id)
    if child:
        chore = next((ch for ch in chores_db if ch['id'] == chore_id), None)
        if chore:
            child['balance'] += chore['reward_amount']
            return jsonify({"status": "success", "new_balance": child['balance']})
    return jsonify({"status": "error", "message": "Chore or child not found"}), 404

@app.route('/redeem_reward', methods=['POST'])
def redeem_reward():
    data = request.json
    child_id = data['child_id']
    reward_id = data['reward_id']
    child = children.get(child_id)
    if child:
        reward = next((rw for rw in rewards_db if rw['id'] == reward_id), None)
        if reward and child['balance'] >= reward['cost']:
            child['balance'] -= reward['cost']
            return jsonify({"status": "success", "new_balance": child['balance']})
    return jsonify({"status": "error", "message": "Reward or child not found, or insufficient balance"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
