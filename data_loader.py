import os
import pandas as pd

class DataLoader:
    def __init__(self, folder_path):
        """
        Inicializa o objeto DataLoader com o caminho da pasta onde os arquivos estão localizados,
        define atributos para os dados como None e carrega automaticamente os arquivos,
        além de realizar os relacionamentos entre as tabelas.

        :param folder_path: Caminho da pasta contendo os arquivos de dados.
        """
        if not os.path.isdir(folder_path):
            raise ValueError("O caminho fornecido não é uma pasta válida.")
        
        self.folder_path = folder_path
        self.sales = None
        self.customer = None
        self.location = None
        self.material = None
        self.plant = None
        self.final_data = None  # Atributo para armazenar os dados combinados

        # Carregar os arquivos automaticamente ao inicializar
        self.load_files()
        self.load_sales_files()

        # Relacionar as tabelas após carregamento dos dados
        self.merge_data()

    def load_files(self):
        """
        Carrega os arquivos CSV principais da pasta e os atribui aos atributos correspondentes.
        """
        file_mapping = {
            "tbl_Customer.csv": "customer",
            "tbl_Location.csv": "location",
            "tbl_Material.csv": "material",
            "tbl_Plant.csv": "plant"
        }

        for file_name, attr in file_mapping.items():
            file_path = os.path.join(self.folder_path, file_name)
            if os.path.exists(file_path):
                setattr(self, attr, pd.read_csv(file_path))
                # print(f"{file_name} carregado com sucesso.")
            else:
                print(f"Aviso: {file_name} não encontrado na pasta especificada.")

    def load_sales_files(self):
        """
        Carrega todos os arquivos mensais de vendas na subpasta 'Sales' e os combina em um único DataFrame.
        """
        sales_folder = os.path.join(self.folder_path, 'Sales')
        if not os.path.isdir(sales_folder):
            print("Aviso: A pasta 'Sales' não foi encontrada.")
            return

        all_sales_data = []  # Lista para armazenar DataFrames de cada arquivo

        # Percorre todos os arquivos na pasta 'Sales'
        for file_name in os.listdir(sales_folder):
            if file_name.endswith('Sales.csv'):
                file_path = os.path.join(sales_folder, file_name)
                monthly_data = pd.read_csv(file_path, parse_dates=['Sales Date'], dayfirst=False, dtype={'Revenue': str, 'Industry': str, 'Order Id': str})
                # monthly_data['Revenue'] = monthly_data['Revenue'].str.replace(',', '.').astype(float)
                monthly_data['Revenue'] = pd.to_numeric(monthly_data['Revenue'].str.replace(',', '.', regex=False), errors='coerce')
                all_sales_data.append(monthly_data)
                # print(f"{file_name} carregado com sucesso.")

        # Concatena todos os arquivos em um único DataFrame, se houver dados
        if all_sales_data:
            self.sales = pd.concat(all_sales_data, ignore_index=True)
            #remove as colunas "Fiscal Year", "Year Month" e "State" da tabela sales
            self.sales.drop(columns=['Fiscal Year', 'Year Month', 'State', 'ID'], inplace=True)

            # Convertendo a coluna 'Sales Date' com o formato específico
            self.sales['Sales Date'] = pd.to_datetime(self.sales['Sales Date'], errors='coerce')
            print("Todos os arquivos de vendas foram combinados com sucesso.")
        else:
            print("Nenhum arquivo de vendas foi encontrado na pasta 'Sales'.")

        # remove vendas negativas
        self.sales = self.sales[self.sales['Revenue'] >= 0]

    def merge_data(self):
        """
        Realiza o merge entre a tabela de vendas (sales) e as tabelas de dimensões (customer, location, material, plant).
        """
        if self.sales is None:
            print("Erro: Tabela de vendas não carregada. Não é possível realizar o merge.")
            return

        # Realizar o merge das tabelas, usando as colunas correspondentes
        try:
            # Relacionar Sales com Customer
            sales_customer = pd.merge(self.sales, self.customer, left_on='Customer Id', right_on='Customer Id', how='left')
            # Relacionar Sales + Customer com Location
            sales_customer_location = pd.merge(sales_customer, self.location, left_on='LOCATION_ID', right_on='LOCATION_ID', how='left')
            # Relacionar Sales + Customer + Location com Material
            sales_customer_location_material = pd.merge(sales_customer_location, self.material, left_on='Product Id', right_on='Product Id', how='left')
            # Relacionar Sales + Customer + Location + Material com Plant
            self.final_data = pd.merge(sales_customer_location_material, self.plant, left_on='Plant', right_on='Plant', how='left')

            print("Todas as tabelas foram relacionadas com sucesso.")
        except KeyError as e:
            print(f"Erro de chave não encontrada ao realizar o merge: {e}")
        except Exception as e:
            print(f"Ocorreu um erro durante o merge dos dados: {e}")

    def get_data(self):
        """
        Método para retornar os dados combinados.
        """
        return self.final_data
