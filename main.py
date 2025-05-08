from webscrp import get_pdfs, download_pdfs
from write_sql import write_sql_vege, write_sql_oth, write_sql_rice, write_sql_fruits, write_sql_fish

def main():
    # download_folder = r"C:\Users\VininduW\Desktop\price list\data"

    # Step 1: Download PDFs
    print("Getting and downloading PDFs...")
    pdf_urls = get_pdfs()
    download_pdfs(pdf_urls)

def write():
    # Step 2: Insert data into DB
    print("Inserting vegetable data...")
    write_sql_vege()

    print("Inserting other items data...")
    write_sql_oth()

    print("Inserting rice data...")
    write_sql_rice()

    print("Inserting fruits data...")
    write_sql_fruits()

    print("Inserting fish data...")
    write_sql_fish()

    print("All done!")

if __name__ == "__main__":
    main()
    write()