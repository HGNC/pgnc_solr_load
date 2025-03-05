import argparse
import asyncio

import pandas
from config import Config
from database import db
from models import (Gene, Symbol)


class GeneDataLoader:
    """
    A class to handle loading and parsing gene data from a CSV file.
    """

    def __init__(self, file_path):
        """
        Initializes the GeneDataLoader with the path to the CSV file.

        :param file_path: Path to the CSV file.
        """
        self.file_path = file_path
        self.df = self.parse_csv()


    def parse_csv(self):
        """
        Parses the CSV file and extracts gene-related data into a pandas DataFrame.

        :return: A pandas DataFrame containing the parsed data, or None if an error occurs.
        """
        try:
            df = pandas.read_csv(self.file_path)
            print("Successfully read CSV file into a DataFrame.")
            return df
        except FileNotFoundError:
            print(f"Error: File not found at path: {self.file_path}")
            return None
        except pandas.errors.EmptyDataError:
            print("Error: The CSV file is empty.")
            return None
        except pandas.errors.ParserError:
            print("Error: Failed to parse the CSV file. It may be malformed.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    async def process_data(self):
        """
        Processes the gene data loaded from the CSV file.

        This method iterates through each row of the DataFrame and extracts specific
        gene-related information.
        """
        if self.df is None:
            print("No data to process. Ensure the CSV file was loaded correctly.")
            return
        await db.set_bind(Config.DATABASE_URI)
        for i in range(len(self.df)):
            row = self.df.iloc[i]
            try:
                potri_id = row["Potri ID"]
                gene = await Gene.get_gene_by_primary(potri_id)
                symbol = await Symbol.create_symbol(row["Approved symbol"])
                print(f"Processing gene with ID: {potri_id} Resulting gene ID: {gene.id} Symbol ID: {symbol.id}")
                exit(1)
            except KeyError as e:
                print(f'Error: CSV file format is incorrect - Key {e}')
                print('Expected columns are "Potri ID, Approved symbol, Approved name , Location, Locus type, NCBI ID - 1, UniProt - 3, PubMed - 4, Name (type alias), Symbol (type alias)"')
                exit(1)


def main():
    """
    Main function to handle command-line arguments and execute CSV parsing and data processing.
    """
    parser = argparse.ArgumentParser(description="Parse a CSV file containing gene data.")
    parser.add_argument("--file", type=str, help="Path to the CSV file.")
    args = parser.parse_args()

    # Load and process the gene data
    data_loader = GeneDataLoader(args.file)
    if data_loader.df is None:
        exit(1)
    asyncio.run(data_loader.process_data())


if __name__ == "__main__":
    main()
