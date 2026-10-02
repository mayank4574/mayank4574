const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const svgFile = process.argv[2] || 'dark.svg';
const outDir = process.argv[3] || 'frames_dark';
const fps = parseInt(process.argv[4] || '12', 10);
const duration = parseFloat(process.argv[5] || '8.0');

if (!fs.existsSync(outDir)) {
  fs.mkdirSync(outDir, { recursive: true });
}

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--force-device-scale-factor=1',
      '--hide-scrollbars',
      '--disable-gpu'
    ]
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1180, height: 610, deviceScaleFactor: 1 });
  
  const absSvg = path.resolve(svgFile).replace(/\\/g, '/');
  await page.goto('file:///' + absSvg);

  const totalFrames = Math.round(duration * fps);
  console.log(`Rendering ${totalFrames} frames for ${svgFile} at ${fps} FPS (${duration}s)...`);

  for (let i = 0; i < totalFrames; i++) {
    const t = i / fps;
    await page.evaluate((currTime) => {
      const svg = document.querySelector('svg');
      if (svg) {
        svg.pauseAnimations();
        svg.setCurrentTime(currTime);
      }
    }, t);

    // Short pause for paint
    await new Promise((r) => setTimeout(r, 20));

    const frameNum = String(i).padStart(4, '0');
    const outPath = path.join(outDir, `frame_${frameNum}.png`);
    await page.screenshot({ path: outPath, type: 'png' });
    if (i % 20 === 0 || i === totalFrames - 1) {
      console.log(`Frame ${i + 1}/${totalFrames} (t=${t.toFixed(2)}s)`);
    }
  }

  await browser.close();
  console.log(`Finished rendering frames to ${outDir}`);
})();
