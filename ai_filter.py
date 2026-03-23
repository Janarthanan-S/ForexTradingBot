
from sklearn.linear_model import LogisticRegression

class AIFilter:

    model = LogisticRegression()
    trained = False

    @staticmethod
    def train(X,y):

        AIFilter.model.fit(X,y)
        AIFilter.trained = True

    @staticmethod
    def predict(features):

        if not AIFilter.trained:
            return 0.5

        prob = AIFilter.model.predict_proba([features])[0][1]

        return prob
