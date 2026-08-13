class Solution:
    def longestRepeating(self, s: str, queryCharacters: str, queryIndices: List[int]) -> List[int]:
        s = list(s)  # convert to list so we can modify characters
        n = len(s)
        
        # segments: SortedList of (start_index) for each maximal same-character run
        # we store segments as (start, end, char) but keep them sorted by start
        segment_starts = SortedList()   # sorted starting indices of segments
        segment_info = {}               # start_index -> (end_index, char)
        
        # lengths: a SortedList (multiset) of all segment lengths,
        # so we can always get the max length in O(log n)
        lengths = SortedList()
        
        # Step 1: Build the initial segments from the original string
        start = 0
        for i in range(1, n + 1):
            if i == n or s[i] != s[start]:
                segment_starts.add(start)
                segment_info[start] = (i - 1, s[start])
                lengths.add(i - start)
                start = i
        
        def remove_segment(seg_start):
            """Helper: remove a segment from all our tracking structures."""
            seg_end, char = segment_info[seg_start]
            segment_starts.remove(seg_start)
            lengths.remove(seg_end - seg_start + 1)
            del segment_info[seg_start]
        
        def add_segment(seg_start, seg_end, char):
            """Helper: add a new segment to all our tracking structures."""
            segment_starts.add(seg_start)
            segment_info[seg_start] = (seg_end, char)
            lengths.add(seg_end - seg_start + 1)
        
        result = []
        
        for idx, new_char in zip(queryIndices, queryCharacters):
            # Step 2: Find which segment currently contains idx
            pos = segment_starts.bisect_right(idx) - 1
            seg_start = segment_starts[pos]
            seg_end, old_char = segment_info[seg_start]
            
            if old_char == new_char:
                # No actual change needed, character is already the same
                result.append(lengths[-1])
                continue
            
            # Step 3: Remove the old segment, since it's about to be split
            remove_segment(seg_start)
            
            # Step 4: Split into up to 3 pieces: [seg_start, idx-1], [idx, idx], [idx+1, seg_end]
            if seg_start <= idx - 1:
                add_segment(seg_start, idx - 1, old_char)
            if idx + 1 <= seg_end:
                add_segment(idx + 1, seg_end, old_char)
            
            # Update the actual character in our string copy
            s[idx] = new_char
            
            # Step 5: The single updated character starts as its own segment
            new_start, new_end = idx, idx
            
            # Step 6: Try merging with the left neighbor segment if same character
            pos = segment_starts.bisect_right(new_start) - 1
            if pos >= 0:
                left_start = segment_starts[pos]
                left_end, left_char = segment_info[left_start]
                if left_end == new_start - 1 and left_char == new_char:
                    remove_segment(left_start)
                    new_start = left_start
            
            # Step 7: Try merging with the right neighbor segment if same character
            pos = segment_starts.bisect_right(new_end)
            if pos < len(segment_starts):
                right_start = segment_starts[pos]
                right_end, right_char = segment_info[right_start]
                if right_start == new_end + 1 and right_char == new_char:
                    remove_segment(right_start)
                    new_end = right_end
            
            # Step 8: Add the final merged segment
            add_segment(new_start, new_end, new_char)
            
            # Step 9: The answer for this query is the largest segment length so far
            result.append(lengths[-1])
        
        return result