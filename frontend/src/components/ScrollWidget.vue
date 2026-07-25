<template>
  <div class="bg-white rounded-sm border border-[#2a1410]/10 shadow-[0_1px_4px_rgba(42,20,16,0.04)] overflow-hidden font-sans flex flex-col h-full">
    
    <div class="flex items-center mb-6 border-b border-[#2a1410]/10 pb-4 px-6 sm:px-8 pt-6 sm:pt-8">
      <h2 class="text-sm font-display font-bold tracking-tight uppercase text-[#2a1410] mr-4"><slot name="title"></slot></h2>
    </div>

    <div class="flex flex-col space-y-4">
      <slot></slot>
    </div>

    <div class="mt-6 pt-4 border-t border-[#2a1410]/5">
      <slot name="footer"></slot>
    </div>

  </div>
</template>

<script>
export default {
  name: 'ScrollWidget'
}
</script>

