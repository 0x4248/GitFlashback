# GitFlashback

Export all Git commits as snapshots.

## Usage

```bash
git clone https://example.com/repo.git the-repo
python -m GitFlashback the-repo/ . -q
```

There should then be a folder called `versions` containing all the snapshots with the corresponding reference.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.