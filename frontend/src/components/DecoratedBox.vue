<template>
  <div class="relative max-w-2xl mx-auto my-8 p-8 sm:p-12 font-serif leading-relaxed text-lg group">
    
    <!-- SVG Filter Definition (Hidden) -->
    <svg width="0" height="0" class="absolute pointer-events-none">
      <defs>
        <filter id="papyrus-torn-edges" x="-20%" y="-20%" width="140%" height="140%">
          <!-- Generate fractal noise for the torn effect -->
          <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="5" result="noise" />
          <!-- Displace the edges of the box using the noise -->
          <feDisplacementMap in="SourceGraphic" in2="noise" scale="12" xChannelSelector="R" yChannelSelector="G" />
        </filter>
      </defs>
    </svg>

    <!-- Shadow wrapper: Applies an outer drop-shadow that perfectly traces the distorted child -->
    <div class="absolute inset-0 z-0 pointer-events-none" style="filter: drop-shadow(4px 8px 12px rgba(0,0,0,0.35))">
      <!-- Background Layer: Has colors, fibers, inner charring, and is distorted by the SVG filter -->
      <div class="absolute inset-0 papyrus-bg"></div>
    </div>

    <!-- Content Layer: Kept separate so the text isn't distorted! -->
    <div class="relative z-10 text-[#3b2b18]">
      <h2 v-if="$slots.heading" class="text-center font-normal mt-0 mb-6 pb-4 border-b border-[#8b4513]/20 text-[#2a1c10] text-3xl font-serif tracking-wide" style="font-family: 'Cinzel', Georgia, serif;">
        <slot name="heading"></slot>
      </h2>
      <div class="space-y-4">
        <slot></slot>
      </div>
    </div>

  </div>
</template>

<script setup>
</script>

<style scoped>
.papyrus-bg {
  /* Papyrus base color from the image */
  background-color: #e8d2b0; 
  
  /* Stains and papyrus fibers */
  background-image: 
    /* Subtle larger stains */
    radial-gradient(circle at 15% 25%, rgba(139, 69, 19, 0.08) 0%, transparent 40%),
    radial-gradient(circle at 85% 75%, rgba(139, 69, 19, 0.08) 0%, transparent 50%),
    /* Horizontal & vertical fibers */
    repeating-linear-gradient(transparent, transparent 3px, rgba(139, 69, 19, 0.035) 3px, rgba(139, 69, 19, 0.035) 4px),
    repeating-linear-gradient(90deg, transparent, transparent 4px, rgba(139, 69, 19, 0.025) 4px, rgba(139, 69, 19, 0.025) 5px);
    
  /* The charring/burn effect on the edges */
  box-shadow: 
    inset 0 0 60px rgba(101, 53, 15, 0.4),   /* Broad browning */
    inset 0 0 20px rgba(60, 25, 0, 0.5),     /* Tighter char */
    inset 0 0 5px rgba(40, 10, 0, 0.7);      /* Sharp burnt edge */

  /* Apply the torn edge distortion */
  filter: url(#papyrus-torn-edges);
  
  /* Give the edges a slight irregularity before distortion */
  border-radius: 4px 8px 3px 6px;
}
</style>
