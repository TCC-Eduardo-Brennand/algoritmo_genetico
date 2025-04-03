import pandas as pd

df = pd.read_parquet(path='Dados/data_final.parquet')

class Circuito():
    def __init__(self, pais):
        self.pais = pais
        self.df = df.loc[(df['Country'] == self.pais) & (df['Year'] == 2022)]
        self.total_voltas = self.buscarTotalVoltas()
        self.media_tempo_pitstop = self.calcularTempoMedioPitstop()
        self.medias_tempos_voltas = self.estimarTemposVoltas()

    def calcularTempoMedioPitstop(self):
        """Calcula o tempo médio do pitstop."""
        df_pitstops = self.df.loc[(self.df['PitStopBool'])]

        # Ordenar os dados pelo nome do piloto e número da volta
        df_pitstops = df_pitstops.sort_values(by=['FullName', 'LapNumber'])

        # Para calcular o tempo de pitstop, obtemos a diferença de tempo entre
        # duas voltas consecutivas
        df_pitstops['TimeDiff'] = df_pitstops.groupby(
            'FullName')['LapTime'].diff()

        # Filtrar apenas as linhas onde há um pitstop (PitStops > 0) e há uma
        # volta anterior (TimeDiff não é NaN) e TimeDiff é maior que 0
        df_pitstops_valido = df_pitstops[
            (df_pitstops['PitStops'] > 0) &
            (df_pitstops['TimeDiff'].notna()) &
            (df_pitstops['TimeDiff'] > 0)]

        # Calcular a média do tempo de pitstop
        tempo_medio_pitstop = df_pitstops_valido['TimeDiff'].mean()

        return round(tempo_medio_pitstop)

    def buscarTotalVoltas(self):
        """Retorna o total de votlas do circuito."""
        return int(self.df['LapNumber'].max())

    def estimarTemposVoltas(self):
        """Estima o tempo de volta de acordo com a degradação do pneu."""
        # Agrupa os dados por Compound e TyreLife p/ calcular media de laptime
        media_tempo_volta_composto_degradacao = self.df.groupby(
            ['Compound', 'TyreLife']).agg({'LapTime': 'mean'}).reset_index()

        # Cria o dicionário no formato desejado
        tempo_volta_dict = media_tempo_volta_composto_degradacao.groupby(
            'Compound')['LapTime'].apply(list).to_dict()

        return tempo_volta_dict