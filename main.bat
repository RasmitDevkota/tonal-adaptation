echo "Data preparation initiated"
echo "- Reducing duplicates..."
python ./reduce_duplicates.py
echo "- Generating translations..."
python ./generate_translations.py
echo "- Verifying translations..."
python ./verify_translations.py
echo "- Extracting features..."
python ./extract_features.py
echo "- Find redundancies..."
python ./find_redundancies.py
echo "- Calculating frequencies..."
python ./calculate_frequencies.py
echo "Data preparation completed!"