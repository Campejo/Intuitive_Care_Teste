from flask import Flask, request, jsonify
from flask_cors import CORS
import csv

app = Flask(__name__)
CORS(app)

def carregar_operadoras(csv_path):
    operadoras = []
    with open(csv_path, 'r', encoding='utf-8', errors='replace') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            operadoras.append(row)
    return operadoras

operadoras_cadastradas = carregar_operadoras('C:\dev\Desafios Vagas\Intuitive_Care_Teste\data_base_project\dados_abertos_gov\operadoras_ativas\Relatorio_cadop.csv')

@app.route('/buscar_operadoras', methods=['GET'])
def buscar_operadoras_rota():
    termo_busca = request.args.get('termo', '')
    resultados = []
    if termo_busca:
        termo_busca = termo_busca.lower()
        for operadora in operadoras_cadastradas:
            for chave, valor in operadora.items():
                if valor and termo_busca in valor.lower():
                    resultado_filtrado = {
                        'Nome_Fantasia': operadora.get('Nome_Fantasia'),
                        'Registro_ANS': operadora.get('Registro_ANS'),
                        'CNPJ': operadora.get('CNPJ')
                    }
                    resultados.append(resultado_filtrado)
                    break # Para evitar adicionar a mesma operadora várias vezes
    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True)