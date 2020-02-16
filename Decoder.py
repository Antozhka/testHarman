import numpy as np

class Alphabet:
    '''Класс алфавита'''
    def __init__(self, filename=None):
        if not filename:
            filename = input('Введите путь к файлу алфавита: ')
        with open(filename, 'r', encoding='utf-8') as f:
            self.characters = f.read()

class Probabilities:
    '''Класс вероятностей'''
    def __init__(self, filename=None):
        if not filename:
            filename = input('Введите путь к файлу вероятностей: ')
        self.probs = np.genfromtxt(filename, delimiter=',')

class BeamEntry:
    "information about one single beam at specific time-step"
    def __init__(self):
        self.prTotal = 0 # blank and non-blank
        self.prNonBlank = 0 # non-blank
        self.prBlank = 0 # blank
        self.labeling = ()

class BeamState:
    "information about the beams at specific time-step"
    def __init__(self):
        self.entries = {}

    def sort(self):
        "return beam-labelings, sorted by probability"
        beams = [v for (_, v) in self.entries.items()]
        sortedBeams = sorted(beams, reverse=True, key=lambda x: x.prTotal)
        return [x.labeling for x in sortedBeams]

def addBeam(beamState, labeling):
    "add beam if it does not yet exist"
    if labeling not in beamState.entries:
        beamState.entries[labeling] = BeamEntry()

class NonCorrectDecoderInput(Exception):
    def __init__(self):
        print('Некорректные входные данные')

class Decoder:
    def __init__(self, alph, probs):
        self.classes = alph.characters
        self.mat = probs.probs
        if len(self.classes) != self.mat.shape[1] - 1:
            raise NonCorrectDecoderInput()

    def ctcBeamSearch(self, beamWidth=25):
        "beam search as described by the paper of Hwang et al. and the paper of Graves et al."

        blankIdx = len(self.classes)
        maxT, maxC = self.mat.shape

        # initialise beam state
        last = BeamState()
        labeling = ()
        last.entries[labeling] = BeamEntry()
        last.entries[labeling].prBlank = 1
        last.entries[labeling].prTotal = 1

        # go over all time-steps
        for t in range(maxT):
            curr = BeamState()

            # get beam-labelings of best beams
            bestLabelings = last.sort()[0:beamWidth]

            # go over best beams
            for labeling in bestLabelings:

                # probability of paths ending with a non-blank
                prNonBlank = 0
                # in case of non-empty beam
                if labeling:
                    # probability of paths with repeated last char at the end
                    prNonBlank = last.entries[labeling].prNonBlank * self.mat[t, labeling[-1]]

                # probability of paths ending with a blank
                prBlank = (last.entries[labeling].prTotal) * self.mat[t, blankIdx]

                # add beam at current time-step if needed
                addBeam(curr, labeling)

                # fill in data
                curr.entries[labeling].labeling = labeling
                curr.entries[labeling].prNonBlank += prNonBlank
                curr.entries[labeling].prBlank += prBlank
                curr.entries[labeling].prTotal += prBlank + prNonBlank


                # extend current beam-labeling
                for c in range(maxC - 1):
                    # add new char to current beam-labeling
                    newLabeling = labeling + (c,)

                    # if new labeling contains duplicate char at the end, only consider paths ending with a blank
                    if labeling and labeling[-1] == c:
                        prNonBlank = self.mat[t, c] * last.entries[labeling].prBlank
                    else:
                        prNonBlank = self.mat[t, c] * last.entries[labeling].prTotal

                    # add beam at current time-step if needed
                    addBeam(curr, newLabeling)

                    # fill in data
                    curr.entries[newLabeling].labeling = newLabeling
                    curr.entries[newLabeling].prNonBlank += prNonBlank
                    curr.entries[newLabeling].prTotal += prNonBlank

            # set new beam state
            last = curr

        # sort by probability
        bestLabeling = last.sort()[0]  # get most probable labeling

        # map labels to chars
        res = ''
        for l in bestLabeling:
            res += self.classes[l]

        return res

def decoder_test():
    alph = Alphabet('test1\\alphabet.txt')
    print(alph.characters)
    probs = Probabilities('test1\\probs.csv')
    print(probs.probs)
    print(Decoder(alph, probs).ctcBeamSearch())
    alph = Alphabet('test2\\alphabet.txt')
    print(alph.characters)
    probs = Probabilities('test2\\probs1.csv')
    print(Decoder(alph, probs).ctcBeamSearch())
    probs = Probabilities('test2\\probs2.csv')
    print(Decoder(alph, probs).ctcBeamSearch())
    probs = Probabilities('test2\\probs3.csv')
    print(Decoder(alph, probs).ctcBeamSearch())

    alph = Alphabet('test1\\alphabet1.txt')
    print(alph.characters)
    probs = Probabilities('test1\\probs.csv')
    print(probs.probs)
    print(Decoder(alph, probs).ctcBeamSearch())


if __name__ == '__main__':
    decoder_test()