"""
HW05 — City Bike Registry (Resizing Chaining Map)
"""

class HashMap:
    """Chaining hash map with auto-resize at load factor > 0.75."""

    def __init__(self, m=4):
        # Create m empty buckets and set size counter
        self.buckets = [[] for _ in range(m)]
        self.count = 0

    # --------------------------------------------------
    def _hash(self, s):
        """Return simple integer hash for string s."""
        h = 0
        for ch in s:
            h = (h * 31 + ord(ch)) % len(self.buckets)
        return h

    # --------------------------------------------------
    def _index(self, key, m=None):
        """Return bucket index for key with current or given bucket count."""
        if m is None:
            m = len(self.buckets)
        h = 0
        for ch in key:
            h = (h * 31 + ord(ch)) % m
        return h

    # --------------------------------------------------
    def __len__(self):
        """Return number of stored pairs."""
        return self.count

    # --------------------------------------------------
    def _resize(self, new_m):
        """Resize to new_m buckets and rehash all pairs."""
        old_items = []
        for bucket in self.buckets:
            for k, v in bucket:
                old_items.append((k, v))
        self.buckets = [[] for _ in range(new_m)]
        self.count = 0
        for k, v in old_items:
            self.put(k, v)

    # --------------------------------------------------
    def put(self, key, value):
        """Insert or overwrite. Resize first if load will exceed 0.75."""
        load_factor = (self.count + 1) / len(self.buckets)
        if load_factor > 0.75:
            self._resize(len(self.buckets) * 2)

        idx = self._hash(key)
        bucket = self.buckets[idx]

        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        self.count += 1

    # --------------------------------------------------
    def get(self, key):
        """Return value for key or None if missing."""
        idx = self._hash(key)
        bucket = self.buckets[idx]
        for k, v in bucket:
            if k == key:
                return v
        return None

    # --------------------------------------------------
    def delete(self, key):
        """Remove key if present. Return True if removed else False."""
        idx = self._hash(key)
        bucket = self.buckets[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.count -= 1
                return True
        return False


if __name__ == "__main__":
    # Optional manual check
    m = HashMap()
    m.put("B1", "S1")
    m.put("B2", "S2")
    print(len(m), m.get("B1"), m.delete("B2"), len(m))
