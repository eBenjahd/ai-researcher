import re

SOCIAL_DOMAINS = {
    "facebook.com",
    "instagram.com",
    "tiktok.com",
    "twitter.com",
    "x.com",
    "linkedin.com",
    "youtube.com",
    "reddit.com",
    "threads.net",
    "quora.com",
}


def get_domain(url):
    match = re.match(
        r"^https?://(?:www\.)?([^/]+)",
        url,
        re.IGNORECASE,
    )

    if match:
        return match.group(1).lower()

    return None


def clean_search_results(search_data):

    query = search_data["query"]
    results = search_data["results"]

    seen_urls = set()
    clean_results = []

    invalid_urls = 0
    social_media = 0
    duplicates = 0

    for result in results:

        url = result.get("url")

        if isinstance(url, str):
            url = url.strip().split("#")[0]
        else:
            url = None

        if (
            not url
            or not url.startswith(("http://", "https://"))
        ):
            invalid_urls += 1
            continue

        domain = get_domain(url)

        if not domain:
            invalid_urls += 1
            continue

        if any(
            domain == social
            or domain.endswith(f".{social}")
            for social in SOCIAL_DOMAINS
        ):
            social_media += 1
            continue

        if url in seen_urls:
            duplicates += 1
            continue

        seen_urls.add(url)

        clean_results.append({
            "id": len(clean_results),
            "title": result.get("title"),
            "url": url,
        })

    return {
        "problem_to_solve": query,
        "stats": {
            "totalResults": len(results),
            "invalidUrls": invalid_urls,
            "socialMedia": social_media,
            "duplicates": duplicates,
            "cleanResults": len(clean_results),
        },
        "results": clean_results,
    }