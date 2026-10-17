# koreanlivingsupport.com – website files

Static site for GitHub Pages: 12 pages (6 English, 6 Korean), no build step needed to publish.

## Upload to GitHub (replace the old one-page site)

1. Open your website repository on GitHub.
2. **Keep the `CNAME` file** (it holds `koreanlivingsupport.com`). Do not delete it.
3. Delete the old `index.html` (or just let the new one overwrite it).
4. Click **Add file → Upload files** and drag in **everything inside this folder**:
   `index.html`, `404.html`, `robots.txt`, `sitemap.xml`, `favicon.png`, `apple-touch-icon.png`,
   and the folders `assets`, `ko`, `expat-housing-chennai`, `frro-visa-services-chennai`,
   `korean-translation-business-support`, `iso-27001-tisax-consulting`, `home-office-it-support-chennai`, `_build`.
5. Write a commit message such as "New multi-page site" and click **Commit changes**.
6. Wait 1–3 minutes, then open https://koreanlivingsupport.com and https://koreanlivingsupport.com/ko/.

## Page addresses

| English | Korean |
| --- | --- |
| / | /ko/ |
| /expat-housing-chennai/ | /ko/chennai-housing/ |
| /frro-visa-services-chennai/ | /ko/frro-visa/ |
| /korean-translation-business-support/ | /ko/business-support/ |
| /iso-27001-tisax-consulting/ | /ko/security-certification/ |
| /home-office-it-support-chennai/ | /ko/it-support/ |

## Changing text later

All text lives in `_build/content.py`. Edit it, then run `python3 _build/build.py` to regenerate every page.
(GitHub Pages ignores the `_build` folder, so it is never shown to visitors.)

## After going live

- Add the site to Google Search Console and submit `https://koreanlivingsupport.com/sitemap.xml`.
- Register on Naver Search Advisor with the same sitemap.
- Replace concept images with real photos when available (same file names in `assets/img/`).
