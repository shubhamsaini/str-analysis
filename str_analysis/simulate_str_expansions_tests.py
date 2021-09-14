import os
import pyfaidx
import tempfile
import unittest

from str_analysis.generate_simulated_bams import generate_synthetic_reference_sequence
from str_analysis.utils.fasta_utils import get_reference_sequence


class Tests(unittest.TestCase):

    def setUp(self):
        self.temp_fasta_file = tempfile.NamedTemporaryFile("w", suffix=".fasta", delete=False)
        self.temp_fasta_file.write(">chrTest1\n")
        self.temp_fasta_file.write("ACGTACGT\n")

        self.temp_fasta_file.write(">chrTest2\n")
        self.temp_fasta_file.write(f"ACGT{'CAG'*2}ACGT\n")
        self.temp_fasta_file.close()

        self.fasta_obj = pyfaidx.Fasta(self.temp_fasta_file.name, one_based_attributes=False, as_raw=True)

    def test_get_reference_sequence(self):
        seq = get_reference_sequence(self.fasta_obj, chrom="chrTest1", start_1based=1, end_1based=5)
        self.assertEqual(seq, "ACGTA")

        seq = get_reference_sequence(self.fasta_obj, chrom="chrTest1", start_1based=8, end_1based=8)
        self.assertEqual(seq, "T")

        seq = get_reference_sequence(self.fasta_obj, chrom="chrTest1", start_1based=8, end_1based=10)
        self.assertEqual(seq, "T")

        seq = get_reference_sequence(self.fasta_obj, chrom="chrTest1", start_1based=9, end_1based=20)
        self.assertEqual(seq, "")

        seq = get_reference_sequence(self.fasta_obj, chrom="chrTest1", start_1based=0, end_1based=1)
        self.assertEqual(seq, "")

    def test_generate_synthetic_reference_sequence(self):
        seq = generate_synthetic_reference_sequence(
            self.fasta_obj, chrom="chrTest2", start_1based=5, end_1based=10, padding_length=4, repeat_unit="CAG", num_copies=0)
        self.assertEqual(seq, "ACGTACGT")

        seq = generate_synthetic_reference_sequence(
            self.fasta_obj, chrom="chrTest2", start_1based=5, end_1based=10, padding_length=2, repeat_unit="CAG", num_copies=0)
        self.assertEqual(seq, "GTAC")

        seq = generate_synthetic_reference_sequence(
            self.fasta_obj, chrom="chrTest2", start_1based=5, end_1based=10, padding_length=2, repeat_unit="CAG", num_copies=3)
        self.assertEqual(seq, "GTCAGCAGCAGAC")

        seq = generate_synthetic_reference_sequence(
            self.fasta_obj, chrom="chrTest2", start_1based=5, end_1based=10, padding_length=2, repeat_unit="CAG", num_copies=10)
        self.assertEqual(seq, "GTCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGAC")

    def tearDown(self):
        if os.path.isfile(self.temp_fasta_file.name):
            os.remove(self.temp_fasta_file.name)


