
def plot_code(df):
    
    from sklearn.feature_extraction.text import TfidfVectorizer
    import umap.umap_ as umap
    import matplotlib.pyplot as plt
    
    # Extracting the required columns
    soft_desc = df['Software Description'].dropna().head(100)
    mit_desc = df['Mitigation Description'].dropna().head(100)
    
    # Preprocessing for embedding using TF/IDF
    vectorizer = TfidfVectorizer(stop_words='english')
    soft_tfidf = vectorizer.fit_transform(soft_desc)
    mit_tfidf = vectorizer.fit_transform(mit_desc)
    
    # Reducing dimensions using UMAP
    soft_embedding = umap.UMAP(n_neighbors=5, min_dist=0.3, metric='cosine').fit_transform(soft_tfidf)
    mit_embedding = umap.UMAP(n_neighbors=5, min_dist=0.3, metric='cosine').fit_transform(mit_tfidf)
    
    # Plotting the result
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    ax[0].scatter(soft_embedding[:, 0], soft_embedding[:, 1])
    ax[0].set_title('Software Description')
    ax[1].scatter(mit_embedding[:, 0], mit_embedding[:, 1])
    ax[1].set_title('Mitigation Description')
    
    return fig
