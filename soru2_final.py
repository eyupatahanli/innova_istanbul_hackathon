import pandas as pd
import random


class GeneticAlgorithm:
    def __init__(self, target, population_number, metrics, target_list):
        self.target = target
        self.population_number = population_number
        self.metrics = metrics
        self.target_list = target_list
        self.population = []

    @staticmethod
    def random_gene():
        """
        metrik değeri hesaplamasında her bir metriğin random oluştuşturulmasına yarar
        ayrıca çaprazlama sırasında meydana gelecek mutasyonlarda da yeni gen (metrik değeri) buradan oluşturulur
        :return: 0-250 arasında bir int sayı
        """
        return random.randint(0, 250)

    def create_chromosome(self):
        """
        metrik değeri için başlangıç kromozomları oluşturur.
        :return: 11 rastgele int değerden oluşan bir dizi
        """
        chromosome = [self.random_gene() for _ in range(11)]
        return chromosome

    def calculate_fitness(self, chromosome):
        """
        kromozom olarak temsil edilen metrik değerlerinin hedefe ne kadar yakın olduğunu hesaplar

        :param chromosome: random üretilen kromozom
        :return: puan, hedefe ne kadar yakın olunduğu
        """
        metrics_copy = self.metrics.copy()
        metrics_copy['METRİK DEĞERİ'] = chromosome
        for col in metrics_copy.columns[2:]:
            metrics_copy[col] = metrics_copy[col] + metrics_copy['METRİK DEĞERİ']

        en_kucuk_indisler = metrics_copy.iloc[0:, 2:].idxmin()
        index_list = []
        for indeks, deger in enumerate(en_kucuk_indisler):
            index_list.append([indeks + 1, deger])

        puan = sum(a == b for a, b in zip(self.target_list, index_list))
        return puan

    def create_population(self):
        """
        popülasyonda istenen kadar sayıda kromozom oluşturur. denenecek metrik değerleri kümesidir
        :return: metrik değerlerinden oluşan bir liste
        """
        for _ in range(self.population_number):
            member = self.create_chromosome()
            self.population.append(member)

    def selection(self):
        """
        populasyonda en yüksek puan değerine sahip yani en sağlıklı genlerin %10 unu sonraki nesle aktarmak için hesaplar
        :return: çaprazlama için seçilen popülasyonun en sağlıklı %10 kromozomu
        """
        fitness_scores = {}
        for i in range(len(self.population)):
            puan = self.calculate_fitness(self.population[i])
            fitness_scores[puan] = self.population[i]
        sorted_fitness_scores = sorted(fitness_scores.items(), key=lambda x: x[0])

        n = len(sorted_fitness_scores)
        end_index = int(n * 0.9)
        selected_values = [value for puan, value in sorted_fitness_scores[end_index:]]
        return selected_values

    def crossover(self):
        """
        en sağlıklı genleri sonraki nesil için belirtilen oranda(%2) rastgele mutasyona uğratır
        ve yeni nesillerden oluşan populasyonu oluşturur.
        :return: yeni nesil olarak nitelendirilen kromozomlar listesi
        """
        next_generation = []
        selected_values = self.selection()

        while len(next_generation) < self.population_number:
            member_1 = random.choice(selected_values)
            member_2 = random.choice(selected_values)
            new_member = []

            for gene1, gene2 in zip(member_1, member_2):
                prob = random.random()  # 0 - 1
                if prob < 0.49:
                    new_member.append(gene1)
                elif prob < 0.98:
                    new_member.append(gene2)
                else:
                    new_member.append(self.random_gene())

            next_generation.append(new_member)

        self.population = next_generation

    def run(self):
        """
        metrik değerlerinin skorunu yani sağlığını hesaplar her 10 iterasyonda ekrana son durumu bastırır
        istenen sağlık durumuna ulaşılması halinde algoritmayı sonlandırır
        :return:
        """
        self.create_population()

        generation_timer = 0
        found_number = None
        highest_score = 0
        best_chromosome = None

        while found_number != self.target:
            self.crossover()
            generation_timer += 1
            found_number = self.calculate_fitness(self.population[0])

            if found_text > highest_score:
                highest_score = found_number
                best_chromosome = self.population[0].copy()

            if generation_timer % 10 == 0:
                print(f"Deneme sayısı: {generation_timer}, En yüksek puan: {highest_score}")
                print(f"En yüksek puan: {highest_score}, Bu puanı sağlayan kromozom: {best_chromosome}")

            if found_number == 24:
                break

        print(f"You found = {found_text}, you did it {generation_timer} steps."
              f"\nYour Target = {self.target}")


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

metrics = pd.read_csv("datasets/Innova-Yapay-Zeka-Soru-2.xlsx - metrics.csv")
metrics = metrics.drop(metrics.index[-1])
beklenen = pd.read_csv("datasets/Innova-Yapay-Zeka-Soru-2.xlsx - beklenen.csv")
beklenen = beklenen.drop(beklenen.index[-1])
data_metrics = pd.read_csv("datasets/Innova-Yapay-Zeka-Soru-2.xlsx - data_metrics.csv")

target_list = []
en_kucuk_indisler = beklenen.iloc[0:, 1:].idxmin()
for indeks, deger in enumerate(en_kucuk_indisler):
    target_list.append([indeks + 1, deger])

target = target_list
population_number = 50

ga = GeneticAlgorithm(target, population_number, metrics, target_list)
ga.run()
