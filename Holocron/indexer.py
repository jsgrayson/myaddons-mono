import os
import psycopg2
import json

def get_db_connection():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    return conn

def generate_lua_index(output_path="Holocron_Index.lua"):
    """
    Queries the database and generates a Lua file containing the inventory index.
    Structure:
    HolocronDB = {
        [ItemID] = {
            name = "Item Name",
            total = 10,
            locations = {
                ["Bag"] = 5,
                ["Bank"] = 5
            }
        }
    }
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Aggregate items by ID and Location Type
        sql = """
            SELECT i.item_id, i.name, s.container_type, SUM(i.count)
            FROM holocron.items i
            JOIN holocron.storage_locations s ON i.location_id = s.location_id
            GROUP BY i.item_id, i.name, s.container_type
        """
        cur.execute(sql)
        rows = cur.fetchall()

        index = {}
        for row in rows:
            item_id = row[0]
            name = row[1]
            container_type = row[2]
            count = row[3]

            if item_id not in index:
                index[item_id] = {
                    "name": name,
                    "total": 0,
                    "locations": {}
                }
            
            index[item_id]["total"] += count
            index[item_id]["locations"][container_type] = count

        cur.close()
        conn.close()

        # Write to Lua file
        with open(output_path, "w") as f:
            f.write("HolocronDB = {\n")
            for item_id, data in index.items():
                # Escape quotes in name
                safe_name = data['name'].replace('"', '\\"')
                f.write(f'    [{item_id}] = {{\n')
                f.write(f'        name = "{safe_name}",\n')
                f.write(f'        total = {data["total"]},\n')
                f.write('        locations = {\n')
                for loc, count in data['locations'].items():
                    f.write(f'            ["{loc}"] = {count},\n')
                f.write('        }\n')
                f.write('    },\n')
            f.write("}\n")

            # Write Jobs Table (Mock data for now as we don't have real GUIDs in DB yet)
            f.write("\nHolocronJobs = {\n")
            # Example format:
            # ["Player-Realm"] = {
            #     { itemID = 12345, count = 5, target = "AuctionAlt" }
            # }
            f.write("}\n")
        
        print(f"Successfully generated {output_path} with {len(index)} items.")

    except Exception as e:
        print(f"Error generating index: {e}")

if __name__ == "__main__":
    # Ensure DB URL is set (for local testing without Docker)
    if 'DATABASE_URL' not in os.environ:
        print("Error: DATABASE_URL environment variable not set.")
    else:
        generate_lua_index()
