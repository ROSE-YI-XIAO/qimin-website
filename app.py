from flask import Flask, render_template, jsonify
import pandas as pd
import networkx as nx
import json

app = Flask(__name__)
def load_knowledge_graph():
    # 读取Excel文件
    df = pd.read_excel('relation.xlsx')
    
    # 创建有向图
    G = nx.DiGraph()
    
    # 添加节点和边
    for _, row in df.iterrows():
        source = row['Subject']
        source_type = row['subject_type']
        target = row['Object']
        target_type = row['object_type']
        relation = row['relation']
        
        # 添加节点时包含节点类型信息
        G.add_node(source, node_type=source_type)
        G.add_node(target, node_type=target_type)
        G.add_edge(source, target, relation=relation)
    
    # 转换为前端所需的数据格式
    nodes = [{"id": node, 
              "name": node,
              "category": G.nodes[node]['node_type'],  # 添加节点类型
              "value": len(list(G.neighbors(node)))    # 添加连接数作为节点大小
            } for node in G.nodes()]
    
    edges = [{"source": u, 
              "target": v, 
              "relation": G[u][v]["relation"]
            } for u, v in G.edges()]
    
    # 获取所有唯一的节点类型
    categories = list(set(node['category'] for node in nodes))
    
    return {
        "nodes": nodes, 
        "edges": edges,
        "categories": [{"name": cat} for cat in categories]
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/graph')
def get_graph():
    graph_data = load_knowledge_graph()
    return jsonify(graph_data)

if __name__ == '__main__':
    app.run(debug=True) 