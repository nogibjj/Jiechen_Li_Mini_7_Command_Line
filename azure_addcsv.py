from azure.cosmos import CosmosClient
import pandas as pd

# Connection details (please replace with your actual values)
URI = "https://command-line-tool.documents.azure.com:443/"
PRIMARY_KEY = (
    "0tR6N3pFDzpMhP9CVNJvH388JThDZVnjUvcVDzFvSBlXrxnNQ2RwA7vh"
    "WjqcG95VkiOazhpciKaRACDbej0QgA=="
)
DATABASE_NAME = "ToDoList"
CONTAINER_NAME = "Items"

# Initialize Cosmos client
client = CosmosClient(URI, PRIMARY_KEY)

# Get database and container
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)


def clear_container():
    """
    Clear out all items in the Cosmos DB container.
    """
    for item in container.query_items(
        query=f"SELECT * FROM {CONTAINER_NAME}", enable_cross_partition_query=True
    ):
        try:
            container.delete_item(item, partition_key=item["id"])
        except Exception as e:
            print(f"Error deleting item with id {item['id']}: {e}")
            continue


def add_dataframe_to_cosmos(df):
    """
    Add the rows of the provided DataFrame to the Cosmos DB container.
    """
    for index, row in df.iterrows():
        item = {
            "id": str(index),
            "location": row["rownames"],
            "rights": row["rights"],
            "network": row["network"],
        }
        add_item(item)


def add_item(item):
    container.upsert_item(item)


def get_item(item_id):
    for item in container.query_items(
        query=f"SELECT * FROM {CONTAINER_NAME} c WHERE c.id = @id",
        parameters=[{"name": "@id", "value": item_id}],
        enable_cross_partition_query=True,
    ):
        return item


if __name__ == "__main__":
    # Load the CSV file into a Pandas DataFrame
    df = pd.read_csv(
        "/Users/castnut/Desktop/706_Data_Engineering/"
        "mini_7/gitclone/Jiechen_Li_Mini_7_Command_Line"
        "/OlympicTV.csv"
    )

    # Clear the old data from the container
    clear_container()

    # Add the new data from the DataFrame
    add_dataframe_to_cosmos(df)

    # Fetch and print the first item as a sample output
    fetched_item = get_item("0")
    print(fetched_item)
