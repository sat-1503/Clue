import itertools

class Sentence:
    def evaluate(self, model):
        raise Exception("Nothing to evaluate")

    def symbols(self):
        return set()

    def formula(self):
        return str(self)


class Symbol(Sentence):
    def __init__(self, name):
        self.name = name

    def evaluate(self, model):
        return model.get(self.name, False)

    def symbols(self):
        return {self.name}

    def __repr__(self):
        return self.name


class Not(Sentence):
    def __init__(self, operand):
        self.operand = operand

    def evaluate(self, model):
        return not self.operand.evaluate(model)

    def symbols(self):
        return self.operand.symbols()

    def __repr__(self):
        return f"¬{self.operand}"


class And(Sentence):
    def __init__(self, *conjuncts):
        self.conjuncts = list(conjuncts)

    def add(self, sentence):
        self.conjuncts.append(sentence)

    def evaluate(self, model):
        return all(c.evaluate(model) for c in self.conjuncts)

    def symbols(self):
        return set().union(*[c.symbols() for c in self.conjuncts])

    def __repr__(self):
        return f"({' ∧ '.join(map(str, self.conjuncts))})"



class Or(Sentence):
    def __init__(self, *disjuncts):
        self.disjuncts = disjuncts

    def evaluate(self, model):
        return any(d.evaluate(model) for d in self.disjuncts)

    def symbols(self):
        return set().union(*[d.symbols() for d in self.disjuncts])

    def __repr__(self):
        return f"({' ∨ '.join(map(str, self.disjuncts))})"


class Implication(Sentence):
    def __init__(self, antecedent, consequent):
        self.antecedent = antecedent
        self.consequent = consequent

    def evaluate(self, model):
        return (not self.antecedent.evaluate(model)) or self.consequent.evaluate(model)

    def symbols(self):
        return self.antecedent.symbols().union(self.consequent.symbols())

    def __repr__(self):
        return f"({self.antecedent} → {self.consequent})"


def model_check(knowledge, query):
    symbols = list(knowledge.symbols().union(query.symbols()))

    def check_all(model, symbols):
        if not symbols:
            if knowledge.evaluate(model):
                return query.evaluate(model)
            return True

        remaining = symbols.copy()
        p = remaining.pop()

        model_true = model.copy()
        model_true[p] = True

        model_false = model.copy()
        model_false[p] = False

        return check_all(model_true, remaining) and check_all(model_false, remaining)

    return check_all({}, symbols)
