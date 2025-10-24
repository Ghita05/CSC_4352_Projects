from collections import defaultdict

class LSH:
    def __init__(self, num_bands, rows_per_band):
        self.num_bands = num_bands
        self.rows_per_band = rows_per_band
        self.buckets = [defaultdict(list) for _ in range(num_bands)]

    def _band_hash(self, band):
        return hash(tuple(band))

    def add_signature(self, item_id, signature):
        for i in range(self.num_bands):
            start = i * self.rows_per_band
            end = start + self.rows_per_band
            band = signature[start:end]
            bucket_key = self._band_hash(band)
            self.buckets[i][bucket_key].append(item_id)

    def find_candidates(self):
        candidates = set()
        for band_dict in self.buckets:
            for ids in band_dict.values():
                if len(ids) > 1:
                    for i in range(len(ids)):
                        for j in range(i + 1, len(ids)):
                            candidates.add(tuple(sorted((ids[i], ids[j]))))
        return candidates
