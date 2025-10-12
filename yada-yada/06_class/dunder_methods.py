class Book:
    def __init__(self,title,pages):
        self.title=title
        self.pages=pages

    def __str__(self):
        return f"{self.title} ({self.pages} pages)"

    def __len__(self):
        return self.pages


b=Book("Python 101",300)
print(str(b))
print(len(b))           