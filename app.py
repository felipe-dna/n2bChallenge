import csv
from PIL import Image


class App:

    # + ---------------------------------------------------------------------- +
    def get_csv(self, path: str) -> object:
        """
        Abre o arquivo passado no parâmetro @path e chama o método map_to_list.j

        @path: recebe o caminho para o arquivo csv

        Após abrir o arquivo, chama o método map_to_list() passando um DictReader
        object que será mapeado e passado para os demais métodos.
        """
        with open(path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            return self.map_to_list(csv_reader)
    # + ---------------------------------------------------------------------- +

    # + ---------------------------------------------------------------------- +
    def map_to_list(self, img_obj: object):
        """
        Recebe um objeto DictReader, itera sobe ele e faz chama os métodos 
        adequados para cada passo.

        @img_obj: recebe o arquivo aberto e lido no método get_csv()

        Itera sobre o objeto, chama o método crop() para criar uma cópia cropada
        de cada imagem que será salva no diretório cropped-imgs e depois chama 
        o método get_histogram() que calcula o histograma do crop. Após isso,
        salva os dados em uma lista que será base para completar a tabela no
        documento csv.
        """
        img_list = []

        for img in img_obj:

            # Fazendo Crop + - - - - - - - - - - - - - - - - - - - - - - - - - -
            img_path = './imgs/{}'.format(img['img'])
            img_name = "cropped-{}-{}".format(img['id'], img['img'])
            coords = int(img['x1']), int(img['y1']), int(
                img['x2']), int(img['y2'])

            crop = self.crop(img_path, img_name, coords)

            # Calculando Histograma + - - - - - - - - - - - - - - - - - - - - -
            histogram = self.get_histogram(crop)

            # Atualizando dados +  - - - - - - - - - - - - - - - - - - -  - - -
            img['result'] = histogram
            img_list.append(img)

            print("> Processando {}".format(img_path))

        # Salvando em um novo csv + - - - - - - - - - - - - - - - - - - - - - -
        self.save_csv(img_list)

    # + ---------------------------------------------------------------------- +

    # + ---------------------------------------------------------------------- +
    def crop(self, img_path: str, img_name: str, coords: tuple) -> str:
        """
        Recebe dados de uma imagem, abre ela como um objeto PIL.Image(), e cria
        uma versão 'cropada' que é salva em './cropped-imgs .j

        @img_path: caminho para a imagem (./imgs/nome-da-img.jpg).
        @img_name: nome que será dado à versão cropada (<id_da_img>-<nome-da-img>.jpg).
        @coords: coordenadas que serão usadas no crop.

        Recebe o caminho para a imagem, o nome final do crop e as coordenadas.
        Após realizar o crop, retorna o caminho para a versão cropada dessa 
        imagem com essas coordenadas.
        """
        cropped_img_path = './cropped-imgs/{}'.format(img_name)

        opened_img = Image.open(img_path)
        cropped_img = opened_img.crop(coords)
        cropped_img.save(cropped_img_path)

        return cropped_img_path
    # + ---------------------------------------------------------------------- +

    # + ---------------------------------------------------------------------- +
    def get_histogram(self, img: str) -> int:
        """
        Recebe o caminho para uma imagem cropada, abre ela como um objeto 
        PIL.Image() e calcula seu histograma.

        @img: caminho para o crop de imagem.

        Retorna o somatório total do histograma encontrado.
        """
        img = Image.open(img)
        histogram_list = img.histogram()

        return sum(histogram_list)
    # + ---------------------------------------------------------------------- +

    # + ---------------------------------------------------------------------- +
    def save_csv(self, img_list: list):
        """
        Abre o arquivo csv, e reescreve o arquivo preenchendo o campo result.

        @img_list: lista com os dados das imagens.
        """

        with open('./arquivos/data.csv', mode='w') as outfile:
            fieldnames = ['id', 'img', 'x1', 'y1',
                          'x2', 'y2', 'result', 'my_result']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in img_list:
                writer.writerow(row)
    # + ---------------------------------------------------------------------- +

    # + ---------------------------------------------------------------------- +
    def run(self):
        self.get_csv('./arquivos/data.csv')
    # + ---------------------------------------------------------------------- +


if __name__ == '__main__':
    app = App()
    app.run()
