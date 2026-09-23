import csv
import os

def generate_sitemap_index(home_url, sitemap_name):
    if home_url.endswith('/'):
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f'<sitemap><loc>{home_url}sitemap.xml</loc></sitemap>\n'
            f'<sitemap><loc>{home_url}hubfs/{sitemap_name}</loc></sitemap>\n'
            '</sitemapindex>'
        )
    else:
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f'<sitemap><loc>{home_url}/sitemap.xml</loc></sitemap>\n'
            f'<sitemap><loc>{home_url}/hubfs/{sitemap_name}</loc></sitemap>\n'
            '</sitemapindex>'
        )

def generate_sitemap(data, urlCol):
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    
    langs = data[2][1:]  # Assuming languages go along the third row from the second column

    for row in data[3:]:
        url = row[urlCol] 
        translations = row[1:] 
        
        if url != "":

            sitemap += f'<url>\n<loc>{url}</loc>\n'
            
            for lang, translation in zip(langs, translations):
                if translation != "":
                    sitemap += f'<xhtml:link rel="alternate" hreflang="{lang}" href="{translation}" />\n'
            
            sitemap += '</url>\n'
    
    sitemap += '</urlset>'
    
    return sitemap

def main():
    # Read data from a CSV file (assuming the file has URLs and translations)
    with open('data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)

    sites = enumerate(data[0:][0])  # list of sites is the first row of data

    for index, site in sites:
        
        if site != "":
    
            sitemap_content = generate_sitemap(data, index)

            home_url = data[3][index]

            sitemap_name = str(site) + '-sitemap.xml'
    
            # Write sitemap content to a file
            os.makedirs('sitemaps', exist_ok=True)

            with open('sitemaps/' + sitemap_name, 'w') as sitemap_file:
                sitemap_file.write(sitemap_content)

            sitemap_index_name = str(site) + '-sitemap-index.xml'
            index_content = generate_sitemap_index(home_url, sitemap_name)
            with open('sitemaps/' + sitemap_index_name, 'w') as index_file:
                index_file.write(index_content)

if __name__ == "__main__":
    main()