import argparse

import pandas
import sqlalchemy as sa
from db.config import Config
from db.enum_types.basic_status import BasicStatusEnum
from db.enum_types.nomenclature import NomenclatureEnum
from db.insert.gene_location import GeneLocation
from db.insert.gene_locus_type import GeneLocusType
from db.insert.gene_name import GeneName
from db.insert.gene_symbol import GeneSymbol
from db.insert.gene_xref import GeneXref
from db.models.gene import Gene
from db.models.user import User


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
            df = pandas.read_csv(
                self.file_path, dtype=str, na_values=["NA", ""], keep_default_na=False
            )
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

    def process_data(self):
        """
        Processes the gene data loaded from the CSV file.

        This method iterates through each row of the DataFrame and extracts specific
        gene-related information.
        """
        if self.df is None:
            print("No data to process. Ensure the CSV file was loaded correctly.")
            return

        # engine = sa.create_engine(Config.DATABASE_URI, echo=True)  # Enable echo to see SQL queries
        engine = sa.create_engine(Config.DATABASE_URI)
        # Use iterrows() to iterate over the DataFrame
        for index, row in self.df.iterrows():
            # Extract data from the row
            primary_id: str | None = row.get("Potri ID", None)

            # Check if the required data is present
            if primary_id is None:
                print(f"Skipping row {index} due to missing data.")
                continue
            session_factory = sa.orm.sessionmaker(bind=engine)
            with session_factory() as session:
                gene_i: Gene = (
                    session.query(Gene)
                    .where(
                        Gene.primary_id == primary_id,
                        Gene.primary_id_source == "phytozome",
                    )
                    .one()
                )
                creator_i: User = (
                    session.query(User).where(User.email == "sart2@cam.ac.uk").one()
                )
                symbol: str | None = row.get("Approved symbol", None)
                if symbol is None:
                    raise ValueError("Approved symbol is required.")
                approved_symbol_i = GeneSymbol(
                    session,
                    symbol,
                    gene_i.id,
                    creator_i.id,
                    NomenclatureEnum.approved,
                    BasicStatusEnum.public,
                )

                alias_symbols: str | None = row.get("Symbol (type alias)", None)
                if alias_symbols is not None and not pandas.isna(alias_symbols):
                    alias_symbol_list: list[str] = alias_symbols.split("|")
                    for alias_symbol in alias_symbol_list:
                        alias_symbol_i = GeneSymbol(
                            session,
                            symbol,
                            gene_i.id,
                            creator_i.id,
                            NomenclatureEnum.alias,
                            BasicStatusEnum.public,
                        )

                name: str | None = row.get("Approved name", None)
                if name is None:
                    raise ValueError("Approved name is required.")
                approved_name_i = GeneName(
                    session,
                    name,
                    gene_i.id,
                    creator_i.id,
                    NomenclatureEnum.approved,
                    BasicStatusEnum.public,
                )

                alias_names: str | None = row.get("Name (type alias)", None)
                if alias_names is not None and not pandas.isna(alias_names):
                    alias_name_list: list[str] = alias_names.split("|")
                    for alias_name in alias_name_list:
                        alias_name_i = GeneName(
                            session,
                            name,
                            gene_i.id,
                            creator_i.id,
                            NomenclatureEnum.alias,
                            BasicStatusEnum.public,
                        )

                location: str | None = row.get("Location", None)
                if location is not None:
                    gene_location_i = GeneLocation(
                        session,
                        location,
                        gene_i.id,
                        creator_i.id,
                        BasicStatusEnum.public,
                    )

                locus_type: str | None = row.get("Locus type", None)
                if locus_type is None:
                    raise ValueError("Locus type is required.")
                gene_locus_type_i = GeneLocusType(
                    session,
                    locus_type,
                    gene_i.id,
                    creator_i.id,
                    BasicStatusEnum.public,
                )

                ncbi_gene_ids: str | None = row.get("NCBI ID - 1", None)
                if ncbi_gene_ids is not None and not pandas.isna(ncbi_gene_ids):
                    ncbi_gene_id_list: list[str] = ncbi_gene_ids.split("|")
                    for ncbi_gene_id in ncbi_gene_id_list:
                        gene_xref_i = GeneXref(
                            session,
                            ncbi_gene_id,
                            1,
                            gene_i.id,
                            creator_i.id,
                            "curator",
                            BasicStatusEnum.public,
                        )

                uniprot_accs: str | None = row.get("UniProt - 3", None)
                if uniprot_accs is not None and not pandas.isna(uniprot_accs):
                    uniprot_acc_list: list[str] = uniprot_accs.split("|")
                    for uniprot_acc in uniprot_acc_list:
                        gene_xref_i = GeneXref(
                            session,
                            uniprot_acc,
                            3,
                            gene_i.id,
                            creator_i.id,
                            "curator",
                            BasicStatusEnum.public,
                        )

                pubmed_ids: str | None = row.get("PubMed - 4", None)
                if pubmed_ids is not None and not pandas.isna(pubmed_ids):
                    pubmed_id_list: list[str] = pubmed_ids.split("|")
                    for pubmed_id in pubmed_id_list:
                        gene_xref_i = GeneXref(
                            session,
                            pubmed_id,
                            4,
                            gene_i.id,
                            creator_i.id,
                            "curator",
                            BasicStatusEnum.public,
                        )

                # session.rollback()
                session.commit()
                print(f"Processed row {index} successfully.")
        print("Data processing complete.")
        engine.dispose()


def main():
    """
    Main function to handle command-line arguments and execute CSV parsing and data processing.
    """
    parser = argparse.ArgumentParser(
        description="Parse a CSV file containing gene data."
    )
    parser.add_argument("--file", type=str, help="Path to the CSV file.")
    args = parser.parse_args()

    # Load and process the gene data
    data_loader = GeneDataLoader(args.file)
    if data_loader.df is None:
        exit(1)
    data_loader.process_data()


if __name__ == "__main__":
    main()
