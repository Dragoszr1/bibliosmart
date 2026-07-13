<template>
  <div class="relative w-full max-w-sm drop-shadow-xl my-6 font-sans">
    
    <!-- Top Rod -->
    <div class="absolute -top-3 left-[-12px] right-[-12px] h-8 bg-gradient-to-b from-[#e8c07d] via-[#fef2cd] to-[#d6a55c] rounded-full shadow-[0_4px_4px_rgba(0,0,0,0.1)] border border-[#cca36b] z-10"></div>
    <div class="absolute -top-3 left-[-12px] w-6 h-8 bg-gradient-to-l from-[#b88034] to-[#8a5a19] rounded-full border border-[#966320] z-20 shadow-inner flex items-center justify-center">
      <div class="w-2.5 h-4 bg-[#4a2e15] rounded-full opacity-80 shadow-inner"></div>
    </div>
    <div class="absolute -top-3 right-[-12px] w-6 h-8 bg-gradient-to-r from-[#b88034] to-[#8a5a19] rounded-full border border-[#966320] z-20 shadow-inner flex items-center justify-center">
      <div class="w-2.5 h-4 bg-[#4a2e15] rounded-full opacity-80 shadow-inner"></div>
    </div>

    <!-- Paper Content -->
    <div 
      class="relative bg-[#fdf5e6] px-6 sm:px-8 py-8 shadow-lg border-x-2 border-[#e3c18b] min-h-[250px] z-0 flex flex-col mx-0"
      style="background-image: repeating-linear-gradient(transparent, transparent 2px, rgba(184, 140, 81, 0.03) 2px, rgba(184, 140, 81, 0.03) 4px);"
    >
      <div class="flex items-center mb-6">
        <h2 class="text-xl font-bold text-[#4a2e15] mr-4 tracking-wide"><slot name="title"></slot></h2>
        <div class="flex-grow h-px bg-[#d1b07d]"></div>
      </div>

      <div class="flex-grow flex flex-col space-y-4">
        <slot></slot>
      </div>

      <div class="mt-6">
        <slot name="footer"></slot>
      </div>
    </div>

    <!-- Bottom Rod -->
    <div class="absolute -bottom-3 left-[-12px] right-[-12px] h-8 bg-gradient-to-t from-[#e8c07d] via-[#fef2cd] to-[#d6a55c] rounded-full shadow-[0_-4px_4px_rgba(0,0,0,0.1)] border border-[#cca36b] z-10"></div>
    <div class="absolute -bottom-3 left-[-12px] w-6 h-8 bg-gradient-to-l from-[#b88034] to-[#8a5a19] rounded-full border border-[#966320] z-20 shadow-inner flex items-center justify-center">
      <div class="w-2.5 h-4 bg-[#4a2e15] rounded-full opacity-80 shadow-inner"></div>
    </div>
    <div class="absolute -bottom-3 right-[-12px] w-6 h-8 bg-gradient-to-r from-[#b88034] to-[#8a5a19] rounded-full border border-[#966320] z-20 shadow-inner flex items-center justify-center">
      <div class="w-2.5 h-4 bg-[#4a2e15] rounded-full opacity-80 shadow-inner"></div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'ScrollWidget'
}
</script>

<style scoped>
</style>
