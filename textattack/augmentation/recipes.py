from . import Augmenter

import textattack

class WordNetAugmenter(Augmenter):
    """ Augments text by replacing with synonyms from the WordNet thesaurus. """
    def __init__(self):
        from textattack.transformations.black_box import WordSwapWordNet
        transformation = WordSwapWordNet()
        super().__init__(transformation, constraints=[])


class EmbeddingAugmenter(Augmenter):
    """ Augments text by transforming words with their embeddings. """
    def __init__(self):
        from textattack.transformations.black_box import WordSwapEmbedding
        transformation = WordSwapEmbedding(
            max_candidates=50, embedding_type='paragramcf'
        )
        from textattack.constraints.semantics import WordEmbeddingDistance
        constraints = [
            WordEmbeddingDistance(min_cos_sim=0.8)
        ]
        super().__init__(transformation, constraints=constraints)
    
    
class CharSwapAugmenter(Augmenter):
    """ Augments words by swapping characters out for other characters. """
    def __init__(self):
        from textattack.transformations import CompositeTransformation
        from textattack.transformations.black_box import \
            WordSwapNeighboringCharacterSwap, \
            WordSwapRandomCharacterDeletion, WordSwapRandomCharacterInsertion, \
            WordSwapRandomCharacterSubstitution, WordSwapNeighboringCharacterSwap
        transformation = CompositeTransformation([
            # (1) Swap: Swap two adjacent letters in the word.
            WordSwapNeighboringCharacterSwap(),
            # (2) Substitution: Substitute a letter in the word with a random letter.
            WordSwapRandomCharacterSubstitution(),
            # (3) Deletion: Delete a random letter from the word.
            WordSwapRandomCharacterDeletion(),
            # (4) Insertion: Insert a random letter in the word.
            WordSwapRandomCharacterInsertion()
        ])
        super().__init__(transformation, constraints=[])