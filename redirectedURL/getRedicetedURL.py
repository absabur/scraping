import pandas as pd
import asyncio
import httpx
import urllib3

# This hides the 'InsecureRequestWarning'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 1. Load your Excel file
input_file = "input.xlsx"
df = pd.read_excel(input_file)

column_name = df.columns[0]
urls = df[column_name].tolist()  # Removed the .head() or test slicing

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# Limit concurrency to 20 at a time so we don't get blocked or crash
sem = asyncio.Semaphore(20)


async def get_final_url(client, url):
    if pd.isna(url) or str(url).strip() == "":
        return "Empty Link"

    clean_url = str(url).strip()
    if not clean_url.startswith("http"):
        clean_url = "https://" + clean_url

    async with sem:  # Use the semaphore here
        try:
            # Added a slightly shorter timeout for speed, and follow_redirects
            response = await client.get(clean_url, follow_redirects=True, timeout=15.0)
            return str(response.url)
        except Exception as e:
            return f"Error: {type(e).__name__}"


async def main():
    print(f"Starting process for {len(urls)} links...")

    async with httpx.AsyncClient(
        headers=HEADERS,
        verify=False,
        limits=httpx.Limits(max_keepalive_connections=5, max_connections=50),
    ) as client:

        tasks = [get_final_url(client, url) for url in urls]

        # This will now process all 4,000+ urls
        results = await asyncio.gather(*tasks)

    # 2. Save back to Excel
    df["Permanent URL"] = results
    output_file = "all_resolved_links.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Finished! All {len(df)} results saved to {output_file}")


if __name__ == "__main__":
    asyncio.run(main())
