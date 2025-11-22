import pandas as pd
import matplotlib.pyplot as plt

class PaperCleaner:
    @property
    def TITLE_COL(self):
        # Field name for the article found in the csv
        return 'Title'
    
    def __init__(self, finder_list=[], desired_domains=[]):
        self.finder_list = finder_list
        self.desired_domains = desired_domains

    # Auxiliary method
    def build_bar_chart(self, categories, values, file_name, title):
        # Create the bar chart
        fig, ax = plt.subplots(figsize=(8, 6))
        bars = ax.bar(categories, values)

        # Annotate each bar with its value
        for bar in bars:
            height = bar.get_height()  # Get the height (value) of the bar
            ax.text(bar.get_x() + bar.get_width() / 2, height,  # X and Y position for text
                    f'{height}', ha='center', va='bottom', fontsize=12)  # Text properties

        # Labeling the chart
        ax.set_xlabel('Categories')
        ax.set_ylabel('Values')
        ax.set_title(title)
        plt.savefig(f"{file_name}.png", dpi=300, bbox_inches="tight")

    # Auxiliary method
    def check_domain(self, link):
        return any(dominio in link for dominio in self.desired_domains)
    
    # Filter method
    def drop_duplicates(self, df):
        # Reveals the duplicated itens if any are found
        duplicates = df[df[self.TITLE_COL].duplicated(keep=False)] # keep=False marks all duplicates
        if len(duplicates) > 0:
            print('Cleaner Stage: found duplicates!')
            print(duplicates)
        
        # Remove duplicates based in TITLE_COL field
        # Keeping the first occurrence and ignoring differences of uppercase and lowercase
        unique_df = df.drop_duplicates(subset=[self.TITLE_COL], keep='first', ignore_index=True)
        unique_df.to_csv('drop_duplicates.csv', index=False)

        categories = ['Before Removal', 'After Removal']
        values = [len(df), len(unique_df)]
        self.build_bar_chart(categories=categories, values=values, file_name='drop_duplicates_chart', title='Removal of Duplicate Articles')

        print('Cleaner Stage: duplicates deleted!')

        return unique_df
    
    # Filter method
    def select_by_article_quality(self):
        # Transforms the list in a DataFrame
        df = pd.DataFrame(self.finder_list, columns=[self.TITLE_COL, 'Link'])
        
        # Check if the link contains one of the desired domains
        filtered_df = df[df['Link'].apply(self.check_domain)]

        # Saves the new filtered DataFrame in a csv file
        filtered_df.to_csv('filtered_domains.csv', index=False)

        categories = ['Before Filter', 'After Filter']
        values = [len(df), len(filtered_df)]
        self.build_bar_chart(categories=categories, values=values, file_name='filtered_domains_chart', title='Selection of Articles by Databases')

        values = []
        for domain in self.desired_domains:
            count =  df['Link'].str.contains(domain.lower()).sum()
            values.append(count)

        self.build_bar_chart(categories=self.desired_domains, values=values, file_name='bases_chart', title='Selection of Articles by Databases')

        print('Cleaner Stage: filtered data!')

        return filtered_df

    # The only method you need to call
    def clean(self):
        filtered_quality = self.select_by_article_quality()
        filtered_duplicates = self.drop_duplicates(filtered_quality)
        return filtered_duplicates

# MAIN

df = pd.read_csv('all_citations.csv')
articles = df.values.tolist()
domains = ['acm', 'ieee', 'springer', 'sciencedirect']
PaperCleaner(articles, domains).clean()
