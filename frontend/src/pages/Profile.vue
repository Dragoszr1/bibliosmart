<template>
  <div id="app" class="font-sans text-[#2a1410] bg-cream min-h-screen pb-20">
    <!-- Hero Section -->
    <section class="relative overflow-hidden border-b border-[#ede0cc] min-h-[240px] flex items-center">
      <div
        class="absolute inset-0"
        style="background: linear-gradient(105deg, rgba(45,16,24,0.95) 0%, rgba(45,16,24,0.85) 100%)"
      ></div>
      <div
        class="absolute inset-0 opacity-[0.03]"
        style="background-image: repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(201,168,76,1) 39px, rgba(201,168,76,1) 40px), repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(201,168,76,1) 39px, rgba(201,168,76,1) 40px)"
      ></div>
      <div class="max-w-7xl mx-auto px-6 py-12 relative w-full text-center sm:text-left z-10">
        <h2 class="text-4xl sm:text-5xl font-black text-white mb-2 tracking-tight drop-shadow font-display uppercase">
          {{ isBibliotecar ? 'Panou Bibliotecar' : 'Profilul Meu' }}
        </h2>
        <div class="flex items-center justify-center sm:justify-start gap-4 w-full opacity-90">
             <div class="h-px flex-1 max-w-[30px] sm:hidden bg-gradient-to-l from-[#c9a84c] to-transparent"></div>
             <p class="text-[#c9a84c] text-sm sm:text-base italic font-serif tracking-widest shrink-0">Bine ai revenit, {{ user.name }}</p>
             <div class="h-px flex-1 max-w-[80px] bg-gradient-to-r from-[#c9a84c] to-transparent"></div>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-6 py-10">
      <!-- Top Row: Profile + Reviews side by side -->
      <div class="grid grid-cols-1 lg:grid-cols-5 gap-6 mb-8">
        <!-- Left: Profile Card -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-sm shadow-[0_1px_4px_rgba(42,20,16,0.04)] border border-[#2a1410]/10 p-5 sm:p-6 h-full flex flex-col">
            <!-- Profile Picture -->
            <div class="flex flex-col items-center mb-5">
              <div class="relative group mb-4">
                <div class="w-28 h-28 rounded-sm bg-cream-dark shadow-sm border border-[#2a1410]/10 overflow-hidden">
                  <img 
                    :src="user.profilePicture" 
                    :alt="user.name"
                    class="w-full h-full object-cover"
                    @error="user.profilePicture = '/api/auth/profile-picture/default'"
                  >
                </div>
                <div 
                  @click="triggerFileInput"
                  class="absolute inset-0 flex items-center justify-center cursor-pointer"
                >
                  <div class="absolute inset-0 bg-dark/60 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center">
                    <i class="pi pi-camera text-white text-xl"></i>
                  </div>
                </div>
                <input 
                  ref="fileInput"
                  type="file"
                  accept="image/png,image/jpeg,image/jpg,image/gif,image/webp"
                  class="hidden"
                  @change="uploadProfilePicture"
                >
              </div>
              <h1 class="text-xl sm:text-2xl font-bold font-display uppercase tracking-tight text-[#2a1410] text-center">{{ user.name }}</h1>
              <!-- Role badge -->
              <span v-if="isBibliotecar" class="mt-2 px-3 py-1 bg-[#c9a84c] text-dark font-mono text-[9px] tracking-widest font-bold uppercase rounded-sm">Bibliotecar</span>
            </div>

            <!-- Description -->
            <div v-if="user.description" class="mb-5 px-2 text-center flex-1">
              <p class="text-[#3b2b18] text-sm font-serif italic leading-relaxed">{{ user.description }}</p>
            </div>
            <div v-else class="mb-5 px-2 text-center flex-1 flex items-center justify-center">
              <p class="text-[#7a5a55] text-sm italic font-serif">Nicio descriere încă.</p>
            </div>

            <!-- Stats -->
            <div class="flex items-center justify-center gap-8 py-5 border-t border-[#2a1410]/10">
              <div class="text-center">
                <p class="text-2xl font-black text-[#2a1410] font-display">{{ user.totalBooksRead }}</p>
                <p class="font-mono text-[10px] tracking-widest uppercase text-[#7a5a55] mt-1">Cărți Citite</p>
              </div>
              <div class="w-px h-10 bg-[#2a1410]/10"></div>
              <div class="text-center">
                <p class="text-2xl font-black text-[#2a1410] font-display">{{ user.userReviews.length }}</p>
                <p class="font-mono text-[10px] tracking-widest uppercase text-[#7a5a55] mt-1">Recenzii</p>
              </div>
            </div>

            <!-- Edit Button -->
            <button @click="openProfileEditModal" class="w-full px-5 py-3 mt-2 rounded-sm font-mono text-xs uppercase tracking-wider transition-colors border border-[#2a1410]/20 text-[#2a1410] hover:bg-[#c9a84c] hover:border-[#c9a84c] font-bold">
              Editează Profil
            </button>
          </div>
        </div>

        <!-- Right: User Reviews -->
        <div class="lg:col-span-3">
          <div class="bg-white rounded-sm shadow-[0_1px_4px_rgba(42,20,16,0.04)] border border-[#2a1410]/10 p-5 sm:p-6 h-full flex flex-col">
            <h2 class="text-sm font-bold font-display uppercase tracking-tight text-[#2a1410] mb-5 flex items-center gap-2">
              <i class="pi pi-star text-[#c9a84c]"></i> Recenziile Mele
            </h2>

            <!-- Loading -->
            <div v-if="loadingReviews" class="flex-1 flex items-center justify-center py-8">
              <i class="pi pi-spin pi-spinner text-2xl text-secondary"></i>
            </div>

            <!-- Empty state -->
            <div v-else-if="user.userReviews.length === 0" class="flex-1 flex flex-col items-center justify-center py-8 border border-dashed border-[#2a1410]/10 rounded-sm bg-cream-dark">
              <i class="pi pi-comments text-3xl text-[#2a1410]/20 mb-3"></i>
              <p class="text-[#7a5a55] font-serif italic text-sm">Nicio recenzie încă</p>
            </div>

            <!-- Reviews list -->
            <div v-else class="flex-1 space-y-4 overflow-y-auto max-h-[400px] pr-2 custom-scrollbar">
              <div v-for="review in user.userReviews" :key="review.id" class="bg-cream rounded-sm p-5 border border-[#2a1410]/5">
                <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-3 mb-2">
                  <div class="min-w-0">
                    <h3 class="text-sm font-bold text-[#2a1410] truncate">{{ review.titlu }}</h3>
                    <p class="font-mono text-[10px] tracking-widest uppercase text-[#7a5a55] mt-1">de {{ review.autor }}</p>
                  </div>
                  <div class="flex items-center gap-1 flex-shrink-0">
                    <span v-for="star in 5" :key="star" :class="star <= review.nota ? 'text-[#c9a84c]' : 'text-[#2a1410]/10'" class="text-[10px]">★</span>
                  </div>
                </div>
                <p class="text-[#3b2b18] text-sm font-serif italic leading-relaxed mt-3">{{ review.comentariu }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Books Read (regular users) -->
      <div v-if="!isBibliotecar">
        <h2 class="text-sm font-bold font-display uppercase tracking-tight text-[#2a1410] mb-5 mt-10 flex items-center gap-2">
          <i class="pi pi-book text-[#c9a84c]"></i> Cărțile Citite
        </h2>

        <div v-if="user.booksRead.length === 0" class="bg-white rounded-sm shadow-[0_1px_4px_rgba(42,20,16,0.04)] border border-[#2a1410]/10 p-8 sm:p-12 text-center">
          <i class="pi pi-book text-4xl sm:text-5xl text-[#2a1410]/20 mb-4 block"></i>
          <p class="text-[#7a5a55] font-serif italic text-sm sm:text-base">Nici o carte citită încă.</p>
        </div>

        <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 sm:gap-5">
          <div 
            v-for="(book, index) in user.booksRead" 
            :key="index"
            class="bg-white rounded-sm border border-[#2a1410]/10 shadow-[0_1px_4px_rgba(42,20,16,0.04)] p-3 text-center hover:shadow-[0_4px_16px_rgba(155,27,48,0.12)] transition-shadow flex flex-col"
          >
            <div class="mb-3 h-32 rounded-sm bg-cream-dark flex items-center justify-center relative overflow-hidden shrink-0 border border-[#2a1410]/5">
              <i class="pi pi-check text-4xl text-[#c9a84c]/50"></i>
            </div>
            <div class="flex-1 flex flex-col justify-end">
                <p class="font-mono text-[9px] uppercase tracking-wider mb-1 text-[#7a5a55] truncate">ISBN: {{ book.ISBN }}</p>
                <h3 class="text-xs font-semibold text-[#2a1410] mb-1 leading-tight line-clamp-2">{{ book.titlu }}</h3>
                <p class="text-[10px] text-[#7a5a55] truncate">{{ book.autor }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- AI Recommendations (regular users only) -->
      <div v-if="!isBibliotecar" class="mt-10">
        <div class="bg-white rounded-sm shadow-[0_1px_4px_rgba(42,20,16,0.04)] border border-[#2a1410]/10 p-5 sm:p-6">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-5">
            <h2 class="text-sm font-bold font-display uppercase tracking-tight text-[#2a1410] flex items-center gap-2">
              <i class="pi pi-sparkles text-[#c9a84c]"></i> Recomandări AI
            </h2>
            <button
              @click="loadAiRecommendations"
              :disabled="loadingAi"
              class="px-5 py-2.5 bg-[#c9a84c] hover:opacity-90 text-dark text-[10px] font-mono tracking-widest uppercase font-bold rounded-sm transition-all disabled:opacity-50 flex items-center justify-center gap-2"
            >
              <i :class="loadingAi ? 'pi pi-spin pi-spinner' : 'pi pi-refresh'"></i>
              {{ aiRecommendations ? 'Reîmprospătează' : 'Generează' }}
            </button>
          </div>

          <div v-if="!aiRecommendations && !loadingAi && !aiError" class="py-10 text-center border border-dashed border-[#2a1410]/10 rounded-sm bg-cream-dark">
            <i class="pi pi-sparkles text-3xl text-[#c9a84c]/50 mb-3 block"></i>
            <p class="text-[#7a5a55] text-sm font-serif italic">Apasă butonul pentru a primi recomandări personalizate bazate pe cărțile tale.</p>
          </div>

          <div v-if="loadingAi" class="py-10 text-center border border-dashed border-[#2a1410]/10 rounded-sm bg-cream-dark">
            <i class="pi pi-spin pi-spinner text-2xl text-[#c9a84c] mb-3 block"></i>
            <p class="text-[#7a5a55] font-mono text-[10px] tracking-widest uppercase">Gemini analizează istoricul tău...</p>
          </div>

          <div v-if="aiError" class="py-4 text-center text-[#ff3d5a] text-xs font-mono bg-[#ff3d5a]/5 rounded-sm">
            <i class="pi pi-exclamation-triangle mr-2"></i>{{ aiError }}
          </div>

          <div v-if="aiRecommendations && !loadingAi" class="bg-cream rounded-sm p-6 border border-[#2a1410]/10">
            <p class="text-[#2a1410] text-sm leading-relaxed whitespace-pre-line font-serif">{{ aiRecommendations }}</p>
          </div>
        </div>
      </div>

      <!-- ═══════════════════════════════════════════════════════════ -->
      <!-- LIBRARIAN PANEL -->
      <!-- ═══════════════════════════════════════════════════════════ -->
      <div v-if="isBibliotecar" class="mt-8">

        <!-- Tab Bar -->
        <div class="flex gap-1 bg-white rounded-sm shadow-[0_1px_4px_rgba(42,20,16,0.04)] border border-[#2a1410]/10 p-1 mb-8 overflow-x-auto custom-scrollbar">
          <button
            v-for="tab in [
              { key: 'cereri',   label: 'Cereri',   icon: 'pi pi-inbox' },
              { key: 'elevi',    label: 'Elevi',    icon: 'pi pi-users' },
              { key: 'anunturi', label: 'Anunțuri', icon: 'pi pi-megaphone' },
              { key: 'club',     label: 'Club',     icon: 'pi pi-bookmark' },
              { key: 'carti',    label: 'Cărți',    icon: 'pi pi-book' },
            ]"
            :key="tab.key"
            @click="changeTab(tab.key)"
            :class="[
              'flex items-center gap-2 px-5 py-2.5 rounded-sm font-mono text-[10px] tracking-widest uppercase transition-all duration-150 whitespace-nowrap flex-shrink-0',
              activeTab === tab.key
                ? 'bg-[#c9a84c] text-dark font-bold'
                : 'text-[#7a5a55] hover:text-[#2a1410] hover:bg-cream-dark font-medium'
            ]"
          >
            <i :class="tab.icon" class="text-xs"></i>
            {{ tab.label }}
            <span v-if="tab.key === 'cereri' && pendingRequestsCount > 0" class="ml-1 bg-white/50 text-[#2a1410] text-[9px] font-bold px-1.5 py-0.5 rounded-sm">{{ pendingRequestsCount }}</span>
            <span v-if="tab.key === 'elevi' && approvedWaitingCount > 0" class="ml-1 bg-[#ff3d5a]/20 text-[#ff3d5a] text-[9px] font-bold px-1.5 py-0.5 rounded-sm border border-[#ff3d5a]/30">{{ approvedWaitingCount }}</span>
          </button>
        </div>

        <!-- tab: cereri -->
        <div v-if="activeTab === 'cereri'" class="mb-8">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
            <h2 class="text-sm font-bold font-display uppercase tracking-tight text-[#2a1410] flex items-center gap-2">
              <i class="pi pi-inbox text-[#c9a84c]"></i> Cereri Împrumut
              <span v-if="pendingRequestsCount > 0" class="ml-2 bg-[#ff3d5a] text-white font-mono text-[9px] px-2 py-0.5 rounded-sm shadow-sm">{{ pendingRequestsCount }}</span>
            </h2>
            <div class="flex gap-2 overflow-x-auto pb-2 sm:pb-0 custom-scrollbar">
              <button
                v-for="f in [{ key: 'all', label: 'Toate' }, { key: 'pending', label: 'În așteptare' }, { key: 'approved', label: 'Aprobate' }, { key: 'ridicat', label: 'Ridicate' }, { key: 'rejected', label: 'Respinse' }]"
                :key="f.key"
                @click="requestFilter = f.key; fetchBookRequests()"
                :class="[
                  'px-4 py-2 rounded-sm font-mono text-[9px] tracking-widest uppercase transition-all whitespace-nowrap',
                  requestFilter === f.key
                    ? 'bg-[#2a1410] text-cream font-bold'
                    : 'bg-white text-[#7a5a55] border border-[#2a1410]/10 hover:border-[#2a1410]/30 hover:text-[#2a1410]'
                ]"
              >
                {{ f.label }}
              </button>
            </div>
          </div>

          <!-- Loading -->
          <div v-if="loadingRequests" class="bg-white rounded-sm shadow-[0_1px_4px_rgba(42,20,16,0.04)] border border-[#2a1410]/10 p-8 text-center">
            <i class="pi pi-spin pi-spinner text-2xl text-[#c9a84c]"></i>
          </div>

          <!-- Empty -->
          <div v-else-if="bookRequests.length === 0" class="bg-white rounded-sm shadow-[0_1px_4px_rgba(42,20,16,0.04)] border border-[#2a1410]/10 p-8 text-center">
            <i class="pi pi-inbox text-3xl text-[#2a1410]/20 mb-3 block"></i>
            <p class="text-[#7a5a55] text-sm font-serif italic">Nicio cerere {{ requestFilter !== 'all' ? 'cu acest status' : '' }}</p>
          </div>

          <!-- Requests List -->
          <div v-else class="space-y-3">
            <div
              v-for="req in bookRequests"
              :key="req.cerere_id"
              :class="[
                'bg-white rounded-sm shadow-[0_1px_4px_rgba(42,20,16,0.04)] border overflow-hidden transition-all',
                req.status === 'pending' ? 'border-[#c9a84c]/50' : req.status === 'approved' ? 'border-[#2a5c3a]/30' : 'border-[#2a1410]/10'
              ]"
            >
              <div class="flex flex-col sm:flex-row sm:items-center gap-4 p-5">
                <!-- Info -->
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-3 mb-2">
                    <span :class="[
                      'font-mono text-[9px] uppercase tracking-widest px-2 py-0.5 rounded-sm font-bold border',
                      req.status === 'pending'   ? 'bg-[#c9a84c]/10 text-[#c9a84c] border-[#c9a84c]/20' :
                      req.status === 'approved'  ? 'bg-[#2a5c3a]/10 text-[#2a5c3a] border-[#2a5c3a]/20' :
                      req.status === 'ridicat' ? 'bg-gray-100 text-gray-600 border-gray-200' :
                      'bg-[#ff3d5a]/10 text-[#ff3d5a] border-[#ff3d5a]/20'
                    ]">
                      {{ { pending: 'În așteptare', approved: 'Aprobat', ridicat: 'Ridicat', rejected: 'Respins' }[req.status] || req.status }}
                    </span>
                    <span class="text-[#7a5a55] font-mono text-[9px] uppercase">{{ formatDate(req.created_at) }}</span>
                  </div>
                  <p class="text-sm font-bold text-[#2a1410] truncate">{{ req.titlu }}</p>
                  <p class="font-mono text-[10px] tracking-widest uppercase text-[#7a5a55] mt-1">de {{ req.autor }}</p>
                  <div class="mt-3 flex items-center gap-2">
                    <div class="w-6 h-6 rounded-sm bg-cream-dark flex items-center justify-center shrink-0 border border-[#2a1410]/10">
                       <i class="pi pi-user text-[#7a5a55] text-[10px]"></i>
                    </div>
                    <p class="text-xs text-[#2a1410] font-medium">
                      {{ req.username }}
                      <span class="ml-1 text-[#7a5a55] font-normal font-serif italic">({{ req.email }})</span>
                    </p>
                  </div>
                </div>

                <!-- Actions (only for pending) -->
                <div v-if="req.status === 'pending'" class="flex gap-2 flex-shrink-0 mt-3 sm:mt-0">
                  <button
                    @click="openPickupModal(req)"
                    class="px-4 py-2.5 bg-[#2a5c3a] hover:bg-[#2a5c3a]/90 text-white font-mono text-[10px] uppercase tracking-widest font-bold rounded-sm transition-colors flex items-center gap-1.5"
                  >
                    <i class="pi pi-check text-[10px]"></i> Aprobă
                  </button>
                  <button
                    @click="handleRequest(req.cerere_id, 'rejected')"
                    class="px-4 py-2.5 bg-white border border-[#ff3d5a]/30 text-[#ff3d5a] hover:bg-[#ff3d5a]/5 font-mono text-[10px] uppercase tracking-widest font-bold rounded-sm transition-colors flex items-center gap-1.5"
                  >
                    <i class="pi pi-times text-[10px]"></i> Respinge
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div><!-- end cereri tab -->

        <!-- tab: cărți -->
        <div v-if="activeTab === 'carti'">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
            <h2 class="text-sm font-bold font-display uppercase tracking-tight text-[#2a1410] flex items-center gap-2">
              <i class="pi pi-cog text-[#c9a84c]"></i> Gestionare Cărți
            </h2>
            <div class="flex gap-3">
              <button
                @click="downloadReport"
                :disabled="downloadingReport"
                class="px-5 py-2.5 bg-white border border-[#2a1410]/20 hover:bg-cream-dark disabled:opacity-60 text-[#2a1410] font-mono text-[10px] uppercase tracking-widest font-bold rounded-sm transition-all flex items-center gap-1.5"
                title="Descarcă raport Word cu toți elevii și împrumuturile lor"
              >
                <i :class="downloadingReport ? 'pi pi-spin pi-spinner' : 'pi pi-file-word'"></i>
                Raport Word
              </button>
              <button @click="openAddBookModal" class="px-5 py-2.5 bg-[#c9a84c] hover:opacity-90 text-dark font-mono text-[10px] uppercase tracking-widest font-bold rounded-sm transition-all flex items-center gap-1.5 shadow-sm">
                <i class="pi pi-plus"></i> Adaugă Carte
              </button>
            </div>
          </div>

          <!-- Search / Filter Bar -->
          <div class="bg-white rounded-sm shadow-[0_1px_4px_rgba(42,20,16,0.04)] border border-[#2a1410]/10 p-5 mb-6">
            <div class="flex flex-col sm:flex-row gap-4">
              <div class="flex-1 flex items-center gap-3 bg-cream-dark rounded-sm px-4 py-3 border border-[#2a1410]/10 focus-within:border-[#c9a84c] transition-colors">
                 <i class="pi pi-search text-[#7a5a55]"></i>
                <input
                  v-model="libSearch"
                  @input="filterLibBooks"
                  type="text"
                  placeholder="Caută carte după titlu, autor, ISBN..."
                  class="bg-transparent border-none focus:outline-none w-full text-sm text-[#2a1410] placeholder-[#7a5a55]/50 font-medium"
                >
              </div>
              <div class="font-mono text-[10px] uppercase tracking-widest text-[#7a5a55] flex items-center shrink-0">
                Total: <span class="text-[#2a1410] font-bold ml-1">{{ filteredLibBooks.length }}</span> cărți
              </div>
            </div>
          </div>

          <!-- Books Table -->
          <div class="bg-white rounded-sm shadow-[0_1px_4px_rgba(42,20,16,0.04)] border border-[#2a1410]/10 overflow-hidden">
            <!-- Loading -->
            <div v-if="loadingBooks" class="flex items-center justify-center py-16">
              <i class="pi pi-spin pi-spinner text-3xl text-[#c9a84c]"></i>
            </div>

            <!-- Table -->
            <div v-else class="overflow-x-auto custom-scrollbar">
              <table class="w-full text-left">
                <thead>
                  <tr class="bg-dark text-cream border-b border-[#2a1410]/10">
                    <th class="px-5 py-4 font-mono text-[10px] tracking-widest uppercase font-bold">Imagine</th>
                    <th class="px-5 py-4 font-mono text-[10px] tracking-widest uppercase font-bold">Titlu / ISBN</th>
                    <th class="px-5 py-4 font-mono text-[10px] tracking-widest uppercase font-bold hidden sm:table-cell">Autor</th>
                    <th class="px-5 py-4 font-mono text-[10px] tracking-widest uppercase font-bold hidden md:table-cell">Gen</th>
                    <th class="px-5 py-4 font-mono text-[10px] tracking-widest uppercase font-bold hidden lg:table-cell">Poziție</th>
                    <th class="px-5 py-4 font-mono text-[10px] tracking-widest uppercase font-bold text-center">Stoc Total</th>
                    <th class="px-5 py-4 font-mono text-[10px] tracking-widest uppercase font-bold text-center">Disponibil</th>
                    <th class="px-5 py-4 font-mono text-[10px] tracking-widest uppercase font-bold text-center">PDF</th>
                    <th class="px-5 py-4 font-mono text-[10px] tracking-widest uppercase font-bold text-center">Acțiuni</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-[#2a1410]/5">
                  <tr 
                    v-for="book in filteredLibBooks" 
                    :key="book.carte_id"
                    class="hover:bg-cream/50 transition-colors"
                  >
                    <!-- Image -->
                    <td class="px-5 py-3">
                      <div class="w-12 h-16 rounded-sm bg-cream border border-[#2a1410]/10 overflow-hidden flex items-center justify-center relative group cursor-pointer" @click="triggerBookImageInput(book.carte_id)">
                        <img 
                          :src="'/api/books/image/' + book.carte_id + '?t=' + imageCacheBust" 
                          class="w-full h-full object-cover"
                          @error="$event.target.style.display='none'"
                        >
                        <i class="pi pi-image text-[#2a1410]/10 text-lg absolute" style="z-index: 0;"></i>
                        <div class="absolute inset-0 bg-dark/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center backdrop-blur-[1px]">
                          <i class="pi pi-camera text-white text-xs"></i>
                        </div>
                      </div>
                    </td>
                    <!-- Title -->
                    <td class="px-5 py-3">
                      <p class="font-semibold text-[#2a1410] text-sm">{{ book.titlu }}</p>
                      <p class="text-[#7a5a55] text-xs sm:hidden font-serif italic mt-0.5">{{ book.autor }}</p>
                      <p class="font-mono text-[9px] uppercase tracking-wider text-[#7a5a55] mt-1">ISBN: {{ book.ISBN }}</p>
                    </td>
                    <!-- Author -->
                    <td class="px-5 py-3 hidden sm:table-cell text-[#3b2b18] text-sm font-serif italic">{{ book.autor }}</td>
                    <!-- Genre -->
                    <td class="px-5 py-3 hidden md:table-cell">
                      <span class="bg-cream-dark text-[#7a5a55] border border-[#2a1410]/10 px-2 py-1 rounded-sm font-mono text-[9px] uppercase tracking-widest font-bold">{{ book.gen }}</span>
                    </td>
                    <!-- Position -->
                    <td class="px-5 py-3 hidden lg:table-cell text-[#7a5a55] text-xs">{{ book.pozitie || '—' }}</td>
                    <!-- Stock Total -->
                    <td class="px-5 py-3 text-center font-bold text-[#2a1410]">{{ book.stoc_total }}</td>
                    <!-- Stock Available -->
                    <td class="px-5 py-3 text-center">
                      <span :class="book.stoc_disponibil > 0 ? 'text-[#2a5c3a] bg-[#2a5c3a]/10 border border-[#2a5c3a]/20' : 'text-[#ff3d5a] bg-[#ff3d5a]/10 border border-[#ff3d5a]/20'" class="font-mono text-[10px] px-2 py-0.5 rounded-sm">{{ book.stoc_disponibil }}</span>
                    </td>
                    <!-- PDF -->
                    <td class="px-5 py-3 text-center">
                      <div class="flex items-center justify-center gap-2">
                        <button v-if="book.has_pdf" @click="openPdfInTab(book.carte_id)" class="p-2 text-[#2a5c3a] hover:bg-[#2a5c3a]/10 rounded-sm transition-colors border border-transparent hover:border-[#2a5c3a]/20" title="Vizualizează PDF">
                          <i class="pi pi-file-pdf text-sm"></i>
                        </button>
                        <button @click="triggerBookPdfInput(book.carte_id)" class="p-2 text-secondary hover:bg-secondary/10 rounded-sm transition-colors border border-transparent hover:border-secondary/20" :title="book.has_pdf ? 'Înlocuiește PDF' : 'Încarcă PDF'">
                          <i :class="book.has_pdf ? 'pi pi-refresh' : 'pi pi-upload'" class="text-sm"></i>
                        </button>
                        <button v-if="book.has_pdf" @click="deleteBookPdf(book)" class="p-2 text-[#ff3d5a] hover:bg-[#ff3d5a]/10 rounded-sm transition-colors border border-transparent hover:border-[#ff3d5a]/20" title="Șterge PDF">
                          <i class="pi pi-times text-sm"></i>
                        </button>
                      </div>
                    </td>
                    <!-- Actions -->
                    <td class="px-5 py-3">
                      <div class="flex items-center justify-center gap-2">
                        <button @click="openEditBookModal(book)" class="p-2 text-[#c9a84c] hover:bg-[#c9a84c]/10 rounded-sm transition-colors border border-transparent hover:border-[#c9a84c]/30" title="Editează">
                          <i class="pi pi-pencil text-sm"></i>
                        </button>
                        <button @click="openStockModal(book)" class="p-2 text-[#2a1410] hover:bg-[#2a1410]/5 rounded-sm transition-colors border border-transparent hover:border-[#2a1410]/10" title="Stoc">
                          <i class="pi pi-sort-alt text-sm"></i>
                        </button>
                        <button @click="confirmDeleteBook(book)" class="p-2 text-[#ff3d5a] hover:bg-[#ff3d5a]/10 rounded-sm transition-colors border border-transparent hover:border-[#ff3d5a]/20" title="Șterge">
                          <i class="pi pi-trash text-sm"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>

              <!-- Empty -->
              <div v-if="filteredLibBooks.length === 0 && !loadingBooks" class="text-center py-16 border-t border-[#2a1410]/5">
                <i class="pi pi-book text-4xl text-[#2a1410]/20 mb-3 block"></i>
                <p class="text-[#7a5a55] font-serif italic text-sm">Nicio carte găsită</p>
              </div>
            </div>
          </div>
        </div><!-- end carti tab -->

        <!-- tab: anunțuri -->
        <div v-if="activeTab === 'anunturi'">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
            <h2 class="text-sm font-bold font-display uppercase tracking-tight text-[#2a1410] flex items-center gap-2">
              <i class="pi pi-megaphone text-[#c9a84c]"></i> Gestionare Anunțuri
            </h2>
            <button @click="openAddAnuntModal" class="px-5 py-2.5 bg-[#c9a84c] hover:opacity-90 text-dark font-mono text-[10px] uppercase tracking-widest font-bold rounded-sm transition-all flex items-center gap-1.5 shadow-sm">
              <i class="pi pi-plus"></i> Anunț Nou
            </button>
          </div>

          <!-- Loading -->
          <div v-if="loadingAnunturi" class="bg-white rounded-sm shadow-[0_1px_4px_rgba(42,20,16,0.04)] border border-[#2a1410]/10 p-8 text-center">
            <i class="pi pi-spin pi-spinner text-2xl text-[#c9a84c]"></i>
          </div>

          <!-- Announcements list -->
          <div v-else class="space-y-4">
            <div 
              v-for="a in allAnunturi" 
              :key="a.anunt_id"
              class="bg-white rounded-sm shadow-[0_1px_4px_rgba(42,20,16,0.04)] border border-[#2a1410]/10 p-5 sm:p-6"
            >
              <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3 mb-4 border-b border-[#2a1410]/10 pb-4">
                <div class="min-w-0 flex-1">
                  <h3 class="text-lg font-bold text-[#2a1410]">{{ a.titlu }}</h3>
                  <p class="font-mono text-[10px] uppercase tracking-widest text-[#7a5a55] mt-2 flex items-center gap-4">
                    <span><i class="pi pi-calendar mr-1.5"></i>{{ a.data_publicare }}</span>
                    <span><i class="pi pi-thumbs-up mr-1.5"></i>{{ a.aprecieri }} aprecieri</span>
                  </p>
                </div>
                <div class="flex gap-2 flex-shrink-0">
                  <button @click="openEditAnuntModal(a)" class="p-2 text-[#c9a84c] hover:bg-[#c9a84c]/10 rounded-sm transition-colors border border-transparent hover:border-[#c9a84c]/30" title="Editează">
                    <i class="pi pi-pencil text-sm"></i>
                  </button>
                  <button @click="confirmDeleteAnunt(a)" class="p-2 text-[#ff3d5a] hover:bg-[#ff3d5a]/10 rounded-sm transition-colors border border-transparent hover:border-[#ff3d5a]/20" title="Șterge">
                    <i class="pi pi-trash text-sm"></i>
                  </button>
                </div>
              </div>
              <p class="text-[#3b2b18] text-sm font-serif italic leading-relaxed whitespace-pre-line">{{ a.anunt }}</p>
            </div>

            <!-- Empty -->
            <div v-if="allAnunturi.length === 0" class="bg-white rounded-sm shadow-[0_1px_4px_rgba(42,20,16,0.04)] border border-[#2a1410]/10 p-12 text-center">
              <i class="pi pi-megaphone text-4xl text-[#2a1410]/20 mb-3 block"></i>
              <p class="text-[#7a5a55] font-serif italic text-sm">Niciun anunț încă</p>
            </div>
          </div>
        </div><!-- end anunturi tab -->

        <!-- tab: elevi -->
        <div v-if="activeTab === 'elevi'">
          <h2 class="text-sm font-bold font-display uppercase tracking-tight text-[#2a1410] flex items-center gap-2 mb-6">
            <i class="pi pi-users text-[#c9a84c]"></i> Gestionare Elevi
          </h2>

          <!-- Two-column layout -->
          <div class="flex flex-col md:flex-row gap-5 min-h-[520px]">

            <!-- LEFT: user list -->
            <div class="w-full md:w-64 flex-shrink-0 bg-white rounded-sm shadow-[0_1px_4px_rgba(42,20,16,0.04)] border border-[#2a1410]/10 flex flex-col overflow-hidden max-h-[600px]">
              <div class="p-3 border-b border-[#2a1410]/10 bg-cream/30">
                <div class="flex items-center gap-2 bg-white rounded-sm px-3 py-2 border border-[#2a1410]/10 focus-within:border-[#c9a84c] transition-colors">
                  <i class="pi pi-search text-[#7a5a55] text-xs"></i>
                  <input
                    v-model="eleviSearch"
                    type="text"
                    placeholder="Caută elev..."
                    class="bg-transparent border-none focus:outline-none w-full text-xs text-[#2a1410] placeholder-[#7a5a55]/50 font-medium"
                  />
                </div>
              </div>
              <div class="flex-1 overflow-y-auto custom-scrollbar">
                <div v-if="loadingElevi" class="flex items-center justify-center py-8 text-[#c9a84c]">
                  <i class="pi pi-spin pi-spinner"></i>
                </div>
                <div v-else-if="eleviFiltrati.length === 0" class="text-center py-8 text-[#7a5a55] font-serif italic text-xs px-3">
                  Niciun utilizator găsit.
                </div>
                <div
                  v-for="u in eleviFiltrati"
                  :key="u.user_id"
                  @click="selecteazaElev(u)"
                  :class="elevSelectat && elevSelectat.user_id === u.user_id
                    ? 'bg-[#c9a84c]/10 border-l-2 border-[#c9a84c]'
                    : 'hover:bg-cream border-l-2 border-transparent'"
                  class="flex items-center gap-3 px-4 py-3 cursor-pointer transition-all border-b border-[#2a1410]/5"
                >
                  <div class="w-8 h-8 rounded-sm bg-cream-dark flex items-center justify-center flex-shrink-0 text-[#2a1410] border border-[#2a1410]/10 font-display font-bold uppercase text-xs">
                    {{ u.username.charAt(0) }}
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-semibold text-[#2a1410] truncate">{{ u.username }}</p>
                    <p class="font-mono text-[9px] uppercase tracking-widest text-[#7a5a55] truncate mt-0.5">{{ u.email }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- RIGHT: selected user detail -->
            <div class="flex-1 bg-white rounded-sm shadow-[0_1px_4px_rgba(42,20,16,0.04)] border border-[#2a1410]/10 overflow-y-auto max-h-[600px] custom-scrollbar">

              <!-- Nothing selected -->
              <div v-if="!elevSelectat" class="flex flex-col items-center justify-center h-full text-[#7a5a55] font-serif italic text-sm py-16">
                <i class="pi pi-arrow-left text-3xl mb-3 text-[#2a1410]/20"></i>
                Selectează un elev din lista din stânga.
              </div>

              <!-- Loading detail -->
              <div v-else-if="loadingElevDetalii" class="flex items-center justify-center h-full py-16">
                <i class="pi pi-spin pi-spinner text-2xl text-[#c9a84c]"></i>
              </div>

              <!-- Detail content -->
              <div v-else-if="elevDetalii" class="p-6 space-y-8">

                <!-- Header user -->
                <div class="flex flex-col sm:flex-row items-center sm:items-start gap-4 p-5 bg-cream rounded-sm border border-[#2a1410]/5">
                  <img
                    :src="`/api/auth/profile-picture/${encodeURIComponent(elevDetalii.user.username)}?t=${imageCacheBust}`"
                    class="w-16 h-16 rounded-sm object-cover border border-[#2a1410]/10 shadow-[0_1px_4px_rgba(42,20,16,0.04)] flex-shrink-0 bg-white"
                    @error="$event.target.src='/api/auth/profile-picture/default'"
                  >
                  <div class="flex-1 min-w-0 text-center sm:text-left">
                    <p class="font-display font-bold text-lg text-[#2a1410] uppercase tracking-tight">{{ elevDetalii.user.username }}</p>
                    <p class="font-mono text-[10px] uppercase tracking-widest text-[#7a5a55] mt-1">{{ elevDetalii.user.email }}</p>
                    <p v-if="elevDetalii.user.telefon" class="text-[#3b2b18] text-xs font-serif italic mt-1.5"><i class="pi pi-phone mr-1"></i>{{ elevDetalii.user.telefon }}</p>
                  </div>
                  <div class="flex-shrink-0 text-center sm:text-right flex sm:block gap-4">
                    <p class="font-mono text-[9px] uppercase tracking-widest text-[#7a5a55]">Ridicat: <span class="font-bold text-[#2a1410] text-xs ml-1">{{ elevDetalii.books_borrowed.length }}</span></p>
                    <p class="font-mono text-[9px] uppercase tracking-widest text-[#7a5a55] sm:mt-1">Citite: <span class="font-bold text-[#2a1410] text-xs ml-1">{{ elevDetalii.books_read.length }}</span></p>
                  </div>
                </div>

                <!-- APROBATE — în așteptarea ridicării fizice -->
                <div>
                  <h3 class="text-sm font-bold font-display uppercase tracking-tight text-[#2a1410] mb-4 flex items-center gap-2 border-b border-[#2a1410]/10 pb-2">
                    <i class="pi pi-clock text-[#c9a84c]"></i> Aprobate — Așteptare ridicare
                    <span v-if="aprovateAsteptare.length" class="ml-2 bg-[#c9a84c]/20 text-[#c9a84c] border border-[#c9a84c]/30 text-[10px] font-bold px-2 py-0.5 rounded-sm">{{ aprovateAsteptare.length }}</span>
                  </h3>
                  <div v-if="aprovateAsteptare.length === 0" class="text-[#7a5a55] font-serif italic text-xs">Nicio carte aprobată în așteptare.</div>
                  <div v-else class="space-y-3">
                    <div v-for="r in aprovateAsteptare" :key="r.cerere_id" class="flex flex-col sm:flex-row sm:items-center gap-4 p-4 border border-[#c9a84c]/30 bg-[#c9a84c]/5 rounded-sm">
                      <div class="w-8 h-8 rounded-sm bg-white border border-[#c9a84c]/20 flex items-center justify-center shrink-0 hidden sm:flex">
                         <i class="pi pi-hourglass text-[#c9a84c]"></i>
                      </div>
                      <div class="flex-1 min-w-0">
                        <p class="text-sm font-semibold text-[#2a1410] truncate">{{ r.titlu }}</p>
                        <p class="font-mono text-[9px] uppercase tracking-widest text-[#7a5a55] mt-1">{{ r.autor }}</p>
                        <p v-if="r.ridicare_de_la" class="text-xs text-[#c9a84c] font-bold mt-2">
                          <i class="pi pi-calendar mr-1"></i>{{ r.ridicare_de_la }} — {{ r.ridicare_pana_la }}
                        </p>
                      </div>
                      <button
                        @click="confirmaRidicare(r.cerere_id)"
                        :disabled="confirmandRidicare === r.cerere_id"
                        class="px-4 py-2.5 bg-[#2a5c3a] hover:bg-[#2a5c3a]/90 disabled:opacity-50 text-white font-mono text-[10px] uppercase tracking-widest font-bold rounded-sm transition-all flex items-center justify-center gap-2 flex-shrink-0"
                      >
                        <i :class="confirmandRidicare === r.cerere_id ? 'pi pi-spin pi-spinner' : 'pi pi-check'"></i>
                        Confirmă ridicarea
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Împrumutate activ (ridicate fizic) -->
                <div>
                  <h3 class="text-sm font-bold font-display uppercase tracking-tight text-[#2a1410] mb-4 flex items-center gap-2 border-b border-[#2a1410]/10 pb-2">
                    <i class="pi pi-book text-[#2a5c3a]"></i> Împrumutate curent
                  </h3>
                  <div v-if="elevDetalii.books_borrowed.length === 0" class="text-[#7a5a55] font-serif italic text-xs">Nicio carte ridicată momentan.</div>
                  <div v-else class="space-y-3">
                    <div v-for="b in elevDetalii.books_borrowed" :key="b.imprumut_id" class="flex flex-col sm:flex-row sm:items-center gap-4 p-4 border border-[#2a5c3a]/20 bg-[#2a5c3a]/5 rounded-sm">
                      <div class="w-8 h-8 rounded-sm bg-white border border-[#2a5c3a]/20 flex items-center justify-center shrink-0 hidden sm:flex">
                        <i class="pi pi-book text-[#2a5c3a]"></i>
                      </div>
                      <div class="flex-1 min-w-0">
                        <p class="text-sm font-semibold text-[#2a1410] truncate">{{ b.titlu }}</p>
                        <p class="font-mono text-[9px] uppercase tracking-widest text-[#7a5a55] mt-1">{{ b.autor }}</p>
                        <div class="mt-2 flex items-center gap-4">
                           <p class="font-mono text-[9px] uppercase tracking-widest text-[#7a5a55]">Ridicat: <span class="text-[#2a1410] font-bold">{{ formatDate(b.borrowed_at) }}</span></p>
                           <p class="font-mono text-[9px] uppercase tracking-widest text-[#ff3d5a]">Scadent: <span class="font-bold">{{ formatDate(b.due_at) }}</span></p>
                        </div>
                      </div>
                      <button
                        @click="deschideReturnareModal(b)"
                        :class="isOverdue(b.due_at) ? 'bg-[#ff3d5a] hover:bg-[#ff3d5a]/90' : 'bg-white border border-[#2a5c3a]/30 text-[#2a5c3a] hover:bg-[#2a5c3a]/5'"
                        class="px-4 py-2.5 font-mono text-[10px] uppercase tracking-widest font-bold rounded-sm transition-all flex items-center justify-center gap-2 flex-shrink-0"
                      >
                        <i class="pi pi-undo"></i>
                        Returnează
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Returnate / citite -->
                <div>
                  <h3 class="text-sm font-bold font-display uppercase tracking-tight text-[#2a1410] mb-4 flex items-center gap-2 border-b border-[#2a1410]/10 pb-2">
                    <i class="pi pi-check-circle text-gray-400"></i> Returnate / citite
                  </h3>
                  <div v-if="elevDetalii.books_read.length === 0" class="text-[#7a5a55] font-serif italic text-xs">Nicio carte returnată.</div>
                  <div v-else class="space-y-3">
                    <div v-for="b in elevDetalii.books_read" :key="b.carte_id" class="flex items-center gap-4 p-4 border border-[#2a1410]/10 bg-cream/30 rounded-sm opacity-80">
                      <div class="w-8 h-8 rounded-sm bg-white border border-[#2a1410]/10 flex items-center justify-center shrink-0">
                         <i class="pi pi-check text-[#7a5a55]"></i>
                      </div>
                      <div class="flex-1 min-w-0">
                        <p class="text-sm font-semibold text-[#2a1410] truncate">{{ b.titlu }}</p>
                        <p class="font-mono text-[9px] uppercase tracking-widest text-[#7a5a55] mt-1">{{ b.autor }}</p>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Istoricul complet cereri -->
                <div>
                  <h3 class="text-sm font-bold font-display uppercase tracking-tight text-[#2a1410] mb-4 flex items-center gap-2 border-b border-[#2a1410]/10 pb-2">
                    <i class="pi pi-history text-[#7a5a55]"></i> Toate cererile
                  </h3>
                  <div v-if="elevDetalii.borrow_history.length === 0" class="text-[#7a5a55] font-serif italic text-xs">Nicio cerere.</div>
                  <div v-else class="space-y-2">
                    <div v-for="r in elevDetalii.borrow_history" :key="r.cerere_id" class="flex items-center gap-3 p-3 border border-[#2a1410]/5 rounded-sm hover:bg-cream-dark transition-colors">
                      <span :class="{
                        'bg-[#c9a84c]/10 text-[#c9a84c] border border-[#c9a84c]/20': r.status === 'pending',
                        'bg-[#2a5c3a]/10 text-[#2a5c3a] border border-[#2a5c3a]/20':   r.status === 'approved',
                        'bg-gray-100 text-gray-500 border border-gray-200': r.status === 'ridicat',
                        'bg-[#ff3d5a]/10 text-[#ff3d5a] border border-[#ff3d5a]/20':     r.status === 'rejected'
                      }" class="font-mono text-[8px] uppercase tracking-widest px-2 py-0.5 rounded-sm font-bold flex-shrink-0">
                        {{ { pending: 'Așteptare', approved: 'Aprobat', ridicat: 'Ridicat', rejected: 'Respins' }[r.status] }}
                      </span>
                      <div class="flex-1 min-w-0">
                        <p class="text-xs font-semibold text-[#2a1410] truncate">{{ r.titlu }}</p>
                        <p class="font-mono text-[8px] uppercase tracking-widest text-[#7a5a55] mt-0.5">{{ r.autor }}</p>
                      </div>
                      <span class="font-mono text-[9px] uppercase tracking-widest text-[#7a5a55] flex-shrink-0">{{ formatDate(r.created_at) }}</span>
                    </div>
                  </div>
                </div>

              </div>
            </div>

          </div>
        </div><!-- end elevi tab -->

        <!-- tab: club -->
        <div v-if="activeTab === 'club'">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
            <h2 class="text-sm font-bold font-display uppercase tracking-tight text-[#2a1410] flex items-center gap-2">
              <i class="pi pi-bookmark text-[#c9a84c]"></i> Invitații Club
            </h2>
            <button
              @click="$router.push('/club/threads')"
              class="px-5 py-2.5 bg-white border border-[#2a1410]/20 hover:bg-cream-dark text-[#2a1410] font-mono text-[10px] uppercase tracking-widest font-bold rounded-sm transition-all flex items-center gap-2"
            >
              <i class="pi pi-comments text-xs"></i> Mergi la discuții
            </button>
          </div>
          <div class="bg-white rounded-sm shadow-[0_1px_4px_rgba(42,20,16,0.04)] border border-[#2a1410]/10 p-6 sm:p-8">
            <p class="text-sm font-serif italic text-[#3b2b18] mb-6">Generează un link de invitație pe care îl poți trimite elevilor. Link-ul îi va adăuga automat în clubul de literatură.</p>
            <div class="flex flex-col sm:flex-row gap-4 sm:items-center mb-6">
              <label class="font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] shrink-0">Valabilitate:</label>
              <div class="flex flex-wrap gap-2">
                  <button
                    v-for="opt in inviteOptions"
                    :key="opt.value"
                    @click="inviteExpiry = opt.value"
                    :class="inviteExpiry === opt.value
                      ? 'bg-[#2a1410] text-white border-[#2a1410]'
                      : 'bg-white text-[#7a5a55] border-[#2a1410]/20 hover:border-[#2a1410]/40 hover:text-[#2a1410]'"
                    class="px-4 py-2 border rounded-sm font-mono text-[9px] uppercase tracking-widest font-bold transition-colors"
                  >
                    {{ opt.label }}
                  </button>
              </div>
            </div>
            <button
              @click="generateInviteLink"
              :disabled="inviteLoading"
              class="px-5 py-3 w-full sm:w-auto bg-[#c9a84c] hover:opacity-90 disabled:opacity-60 text-dark font-mono text-[10px] uppercase tracking-widest font-bold rounded-sm transition-all flex items-center justify-center gap-2"
            >
              <i :class="inviteLoading ? 'pi pi-spin pi-spinner' : 'pi pi-link'"></i>
              Generează link
            </button>
            <div v-if="generatedInviteLink" class="mt-6 p-5 border border-[#c9a84c]/30 bg-[#c9a84c]/5 rounded-sm">
              <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-3">Link generat (expiră {{ inviteExpiresAt }}):</label>
              <div class="flex flex-col sm:flex-row gap-3">
                <input
                  :value="generatedInviteLink"
                  readonly
                  class="flex-1 px-4 py-2.5 bg-white border border-[#2a1410]/20 rounded-sm font-mono text-xs text-[#2a1410] focus:outline-none"
                />
                <button
                  @click="copyInviteLink"
                  class="px-5 py-2.5 bg-white border border-[#2a1410]/20 hover:bg-cream-dark text-[#2a1410] font-mono text-[10px] uppercase tracking-widest font-bold rounded-sm transition-colors flex items-center justify-center gap-2"
                >
                  <i :class="inviteCopied ? 'pi pi-check text-[#2a5c3a]' : 'pi pi-copy'"></i>
                  {{ inviteCopied ? 'Copiat!' : 'Copiază' }}
                </button>
              </div>
            </div>
            <div v-if="inviteError" class="mt-4 p-3 bg-[#ff3d5a]/5 border border-[#ff3d5a]/20 rounded-sm">
              <p class="text-[#ff3d5a] font-mono text-[10px] uppercase tracking-widest">{{ inviteError }}</p>
            </div>
          </div>
          
          <h2 class="text-sm font-bold font-display uppercase tracking-tight text-[#2a1410] flex items-center gap-2 mt-10 mb-5">
            <i class="pi pi-comments text-[#c9a84c]"></i> Discuții în așteptare
          </h2>
          <div class="bg-white rounded-sm shadow-[0_1px_4px_rgba(42,20,16,0.04)] border border-[#2a1410]/10 p-6 sm:p-8">
            <div v-if="pendingThreadsLoading" class="text-center py-8">
              <i class="pi pi-spin pi-spinner text-[#c9a84c] text-2xl"></i>
            </div>
            <div v-else-if="pendingThreads.length === 0" class="text-center py-8 text-[#7a5a55] font-serif italic text-sm">
              Nicio discuție în așteptare.
            </div>
            <div v-else class="space-y-4">
              <div v-for="thread in pendingThreads" :key="thread.thread_id" class="border border-[#2a1410]/10 rounded-sm p-5 bg-cream">
                <div class="flex flex-col sm:flex-row justify-between items-start gap-5">
                  <div class="flex-1">
                    <h3 class="font-bold text-[#2a1410]">{{ thread.titlu }}</h3>
                    <p class="font-mono text-[9px] uppercase tracking-widest text-[#7a5a55] mt-1 mb-3">Propus de <b class="text-[#2a1410]">{{ thread.autor }}</b> • {{ formatDate(thread.creat_la) }}</p>
                    <p class="text-sm font-serif italic text-[#3b2b18] whitespace-pre-line">{{ thread.continut }}</p>
                  </div>
                  <div class="flex flex-row sm:flex-col gap-2 flex-shrink-0 w-full sm:w-auto mt-4 sm:mt-0">
                    <button @click="approveThread(thread.thread_id)" class="flex-1 sm:flex-none px-4 py-2 bg-[#2a5c3a] hover:bg-[#2a5c3a]/90 text-white rounded-sm font-mono text-[9px] uppercase tracking-widest font-bold transition-colors flex items-center justify-center gap-1.5"><i class="pi pi-check"></i> Aprobă</button>
                    <button @click="rejectThread(thread.thread_id)" class="flex-1 sm:flex-none px-4 py-2 bg-white border border-[#ff3d5a]/30 text-[#ff3d5a] hover:bg-[#ff3d5a]/5 rounded-sm font-mono text-[9px] uppercase tracking-widest font-bold transition-colors flex items-center justify-center gap-1.5"><i class="pi pi-times"></i> Respinge</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div><!-- end club tab -->

      </div>
    </main>

    <!-- Hidden file input for book images -->
    <input ref="bookImageInput" type="file" accept="image/png,image/jpeg,image/jpg,image/gif,image/webp" class="hidden" @change="uploadBookImage">
    <!-- Hidden file input for book PDFs -->
    <input ref="bookPdfInput" type="file" accept="application/pdf" class="hidden" @change="uploadBookPdf">

    <!-- MODALS -->

    <!-- Pickup Interval Modal (approve book request) -->
    <div v-if="pickupModalOpen" class="fixed inset-0 z-[60] flex items-center justify-center p-4" @click.self="pickupModalOpen = false">
      <div class="absolute inset-0 bg-dark/60 backdrop-blur-sm" @click="pickupModalOpen = false"></div>
      <div class="relative w-full max-w-md bg-white rounded-sm shadow-[0_4px_24px_rgba(42,20,16,0.1)] border border-[#2a1410]/10 p-6 sm:p-8 z-10">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-sm font-bold font-display uppercase tracking-tight text-[#2a1410] flex items-center gap-2">
            <i class="pi pi-calendar-plus text-[#2a5c3a]"></i> Aprobă cerere
          </h2>
          <button @click="pickupModalOpen = false" class="text-[#7a5a55] hover:text-[#2a1410] text-2xl font-bold leading-none transition-colors">&times;</button>
        </div>

        <div class="bg-cream rounded-sm p-4 mb-6 border border-[#2a1410]/10">
          <p class="text-sm font-bold text-[#2a1410] truncate">{{ pickupReq.titlu }}</p>
          <p class="font-mono text-[10px] uppercase tracking-widest text-[#7a5a55] mt-1">de {{ pickupReq.autor }}</p>
          <div class="mt-3 flex items-center gap-2">
            <div class="w-6 h-6 rounded-sm bg-cream-dark flex items-center justify-center shrink-0 border border-[#2a1410]/10">
               <i class="pi pi-user text-[#7a5a55] text-[10px]"></i>
            </div>
            <p class="text-xs text-[#2a1410] font-medium">
              {{ pickupReq.username }}
              <span class="ml-1 text-[#7a5a55] font-normal font-serif italic">({{ pickupReq.email }})</span>
            </p>
          </div>
        </div>

        <p class="text-sm font-serif italic text-[#3b2b18] mb-5">Alege intervalul în care elevul poate ridica cartea. Un email de confirmare va fi trimis automat.</p>

        <div class="space-y-4">
          <div>
            <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-2">De la</label>
            <div class="flex gap-3">
              <input v-model="pickupFromDate" type="date" class="flex-1 px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-mono text-xs text-[#2a1410] focus:outline-none transition-colors">
              <input
                v-model="pickupFromTime"
                type="text"
                placeholder="HH:MM"
                maxlength="5"
                @input="formatTimeInput('pickupFromTime', $event)"
                class="w-24 px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-mono text-xs text-[#2a1410] text-center focus:outline-none transition-colors"
              >
            </div>
          </div>
          <div>
            <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-2">Până la</label>
            <div class="flex gap-3">
              <input v-model="pickupUntilDate" type="date" class="flex-1 px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-mono text-xs text-[#2a1410] focus:outline-none transition-colors">
              <input
                v-model="pickupUntilTime"
                type="text"
                placeholder="HH:MM"
                maxlength="5"
                @input="formatTimeInput('pickupUntilTime', $event)"
                class="w-24 px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-mono text-xs text-[#2a1410] text-center focus:outline-none transition-colors"
              >
            </div>
          </div>
        </div>

        <p v-if="pickupError" class="text-[10px] font-mono tracking-widest uppercase text-[#ff3d5a] mt-4">{{ pickupError }}</p>

        <div class="flex flex-col sm:flex-row gap-3 mt-8">
          <button
            @click="pickupModalOpen = false"
            class="flex-1 px-5 py-3 bg-white border border-[#2a1410]/20 text-[#2a1410] font-mono text-[10px] uppercase tracking-widest font-bold rounded-sm hover:bg-cream-dark transition-colors"
          >
            Anulează
          </button>
          <button
            @click="confirmApprove"
            :disabled="approvingRequest"
            class="flex-[2] px-5 py-3 bg-[#2a5c3a] hover:bg-[#2a5c3a]/90 disabled:opacity-60 text-white font-mono text-[10px] uppercase tracking-widest font-bold rounded-sm transition-colors flex items-center justify-center gap-2"
          >
            <i :class="approvingRequest ? 'pi pi-spin pi-spinner' : 'pi pi-check'"></i>
            Aprobă & Trimite Email
          </button>
        </div>
      </div>
    </div>

    <!-- Edit Profile Modal -->
    <div v-if="editProfileOpen" class="fixed inset-0 z-[60] flex items-center justify-center p-4" @click.self="editProfileOpen = false">
      <div class="absolute inset-0 bg-dark/60 backdrop-blur-sm" @click="editProfileOpen = false"></div>
      <div class="relative w-full max-w-lg bg-white rounded-sm shadow-[0_4px_24px_rgba(42,20,16,0.1)] border border-[#2a1410]/10 p-6 sm:p-8 z-10">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-sm font-bold font-display uppercase tracking-tight text-[#2a1410]">Editează Profil</h2>
          <button @click="editProfileOpen = false" class="text-[#7a5a55] hover:text-[#2a1410] text-2xl font-bold transition-colors duration-200 leading-none">&times;</button>
        </div>
        <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-2">Descriere personală</label>
        <textarea
          v-model="editDescription"
          rows="5"
          maxlength="255"
          placeholder="Scrie ceva despre tine..."
          class="w-full px-4 py-3 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-serif text-sm text-[#2a1410] placeholder-[#7a5a55]/50 focus:outline-none transition-colors resize-none"
        ></textarea>
        <p class="text-[#7a5a55] font-mono text-[9px] uppercase tracking-widest mt-2 text-right">{{ editDescription.length }} / 255</p>
        <div v-if="profileMsg.error" class="mt-4 p-3 bg-[#ff3d5a]/5 border border-[#ff3d5a]/20 rounded-sm">
          <p class="text-[#ff3d5a] font-mono text-[10px] uppercase tracking-widest">{{ profileMsg.error }}</p>
        </div>
        <div v-if="profileMsg.success" class="mt-4 p-3 bg-[#2a5c3a]/5 border border-[#2a5c3a]/20 rounded-sm">
          <p class="text-[#2a5c3a] font-mono text-[10px] uppercase tracking-widest">{{ profileMsg.success }}</p>
        </div>
        <div class="mt-8 flex flex-col sm:flex-row gap-3">
          <button @click="saveDescription" :disabled="savingDescription" class="flex-[2] px-5 py-3 bg-[#c9a84c] text-dark hover:opacity-90 font-mono text-[10px] uppercase tracking-widest font-bold rounded-sm disabled:opacity-50 disabled:cursor-not-allowed transition-all">
            {{ savingDescription ? 'Se salvează...' : 'Salvează Modificări' }}
          </button>
          <button @click="editProfileOpen = false" class="flex-1 px-5 py-3 bg-white border border-[#2a1410]/20 text-[#2a1410] font-mono text-[10px] uppercase tracking-widest font-bold rounded-sm hover:bg-cream-dark transition-colors">
            Anulează
          </button>
        </div>
      </div>
    </div>

    <!-- Add Book Modal -->
    <div v-if="addBookOpen" class="fixed inset-0 z-[60] flex items-center justify-center p-4" @click.self="addBookOpen = false">
      <div class="absolute inset-0 bg-dark/60 backdrop-blur-sm" @click="addBookOpen = false"></div>
      <div class="relative bg-white rounded-sm shadow-[0_4px_24px_rgba(42,20,16,0.1)] border border-[#2a1410]/10 w-full max-w-lg z-10 p-6 sm:p-8 max-h-[90vh] overflow-y-auto custom-scrollbar">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-sm font-bold font-display uppercase tracking-tight text-[#2a1410]">Adaugă Carte Nouă</h2>
          <button @click="addBookOpen = false" class="text-[#7a5a55] hover:text-[#2a1410] text-2xl font-bold leading-none">&times;</button>
        </div>
        <form @submit.prevent="submitAddBook" class="space-y-5">
          <div>
            <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-2">Titlu *</label>
            <input v-model="addForm.titlu" type="text" required class="w-full px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-sans text-sm text-[#2a1410] focus:outline-none transition-colors">
          </div>
          <div>
            <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-2">Autor *</label>
            <input v-model="addForm.autor" type="text" required class="w-full px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-sans text-sm text-[#2a1410] focus:outline-none transition-colors">
          </div>
          <div>
            <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-2">ISBN *</label>
            <input v-model="addForm.ISBN" type="text" required maxlength="13" class="w-full px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-mono text-xs text-[#2a1410] focus:outline-none transition-colors">
          </div>
          <div>
            <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-2">Gen *</label>
            <input v-model="addForm.gen" type="text" required class="w-full px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-sans text-sm text-[#2a1410] focus:outline-none transition-colors">
          </div>
          <div>
            <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-2">Poziție în bibliotecă</label>
            <input v-model="addForm.pozitie" type="text" placeholder="ex: Raft A3, Sala 2" class="w-full px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-sans text-sm text-[#2a1410] placeholder-[#7a5a55]/50 focus:outline-none transition-colors">
          </div>
          <div>
            <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-2">Cod</label>
            <input v-model="addForm.cod" type="text" placeholder="ex: BIO-042" class="w-full px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-mono text-xs text-[#2a1410] placeholder-[#7a5a55]/50 focus:outline-none transition-colors">
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-2">Stoc Total</label>
              <input v-model.number="addForm.stoc_total" type="number" min="0" class="w-full px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-sans text-sm text-[#2a1410] focus:outline-none transition-colors">
            </div>
            <div>
              <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-2">Stoc Disponibil</label>
              <input v-model.number="addForm.stoc_disponibil" type="number" min="0" class="w-full px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-sans text-sm text-[#2a1410] focus:outline-none transition-colors">
            </div>
          </div>
          <div v-if="addMsg.error" class="p-3 bg-[#ff3d5a]/5 border border-[#ff3d5a]/20 rounded-sm">
            <p class="text-[#ff3d5a] font-mono text-[10px] uppercase tracking-widest">{{ addMsg.error }}</p>
          </div>
          <div v-if="addMsg.success" class="p-3 bg-[#2a5c3a]/5 border border-[#2a5c3a]/20 rounded-sm">
            <p class="text-[#2a5c3a] font-mono text-[10px] uppercase tracking-widest">{{ addMsg.success }}</p>
          </div>
          <button type="submit" class="w-full px-5 py-3 mt-4 bg-[#c9a84c] text-dark hover:opacity-90 font-mono text-[10px] uppercase tracking-widest font-bold rounded-sm transition-all shadow-sm">
            Adaugă Carte
          </button>
        </form>
      </div>
    </div>

    <!-- Edit Book Modal -->
    <div v-if="editBookOpen" class="fixed inset-0 z-[60] flex items-center justify-center p-4" @click.self="editBookOpen = false">
      <div class="absolute inset-0 bg-dark/60 backdrop-blur-sm" @click="editBookOpen = false"></div>
      <div class="relative bg-white rounded-sm shadow-[0_4px_24px_rgba(42,20,16,0.1)] border border-[#2a1410]/10 w-full max-w-lg z-10 p-6 sm:p-8 max-h-[90vh] overflow-y-auto custom-scrollbar">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-sm font-bold font-display uppercase tracking-tight text-[#2a1410]">Editează Carte</h2>
          <button @click="editBookOpen = false" class="text-[#7a5a55] hover:text-[#2a1410] text-2xl font-bold leading-none">&times;</button>
        </div>
        <form @submit.prevent="submitEditBook" class="space-y-5">
          <div>
            <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-2">Titlu</label>
            <input v-model="editBookForm.titlu" type="text" class="w-full px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-sans text-sm text-[#2a1410] focus:outline-none transition-colors">
          </div>
          <div>
            <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-2">Autor</label>
            <input v-model="editBookForm.autor" type="text" class="w-full px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-sans text-sm text-[#2a1410] focus:outline-none transition-colors">
          </div>
          <div>
            <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-2">ISBN</label>
            <input v-model="editBookForm.ISBN" type="text" maxlength="13" class="w-full px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-mono text-xs text-[#2a1410] focus:outline-none transition-colors">
          </div>
          <div>
            <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-2">Gen</label>
            <input v-model="editBookForm.gen" type="text" class="w-full px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-sans text-sm text-[#2a1410] focus:outline-none transition-colors">
          </div>
          <div>
            <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-2">Poziție în bibliotecă</label>
            <input v-model="editBookForm.pozitie" type="text" placeholder="ex: Raft A3, Sala 2" class="w-full px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-sans text-sm text-[#2a1410] placeholder-[#7a5a55]/50 focus:outline-none transition-colors">
          </div>
          <div>
            <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-2">Cod</label>
            <input v-model="editBookForm.cod" type="text" placeholder="ex: BIO-042" class="w-full px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-mono text-xs text-[#2a1410] placeholder-[#7a5a55]/50 focus:outline-none transition-colors">
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-2">Stoc Total</label>
              <input v-model.number="editBookForm.stoc_total" type="number" min="0" class="w-full px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-sans text-sm text-[#2a1410] focus:outline-none transition-colors">
            </div>
            <div>
              <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-2">Stoc Disponibil</label>
              <input v-model.number="editBookForm.stoc_disponibil" type="number" min="0" class="w-full px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-sans text-sm text-[#2a1410] focus:outline-none transition-colors">
            </div>
          </div>
          <div v-if="editBookMsg.error" class="p-3 bg-[#ff3d5a]/5 border border-[#ff3d5a]/20 rounded-sm">
            <p class="text-[#ff3d5a] font-mono text-[10px] uppercase tracking-widest">{{ editBookMsg.error }}</p>
          </div>
          <div v-if="editBookMsg.success" class="p-3 bg-[#2a5c3a]/5 border border-[#2a5c3a]/20 rounded-sm">
            <p class="text-[#2a5c3a] font-mono text-[10px] uppercase tracking-widest">{{ editBookMsg.success }}</p>
          </div>
          <button type="submit" class="w-full px-5 py-3 mt-4 bg-[#c9a84c] text-dark hover:opacity-90 font-mono text-[10px] uppercase tracking-widest font-bold rounded-sm transition-all shadow-sm">
            Salvează Modificări
          </button>
        </form>
      </div>
    </div>

    <!-- Quick Stock Modal -->
    <div v-if="stockModalOpen" class="fixed inset-0 z-[60] flex items-center justify-center p-4" @click.self="stockModalOpen = false">
      <div class="absolute inset-0 bg-dark/60 backdrop-blur-sm" @click="stockModalOpen = false"></div>
      <div class="relative bg-white rounded-sm shadow-[0_4px_24px_rgba(42,20,16,0.1)] border border-[#2a1410]/10 w-full max-w-sm z-10 p-6 sm:p-8">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-sm font-bold font-display uppercase tracking-tight text-[#2a1410]">Actualizare Stoc</h2>
          <button @click="stockModalOpen = false" class="text-[#7a5a55] hover:text-[#2a1410] text-2xl font-bold leading-none">&times;</button>
        </div>
        <p class="text-[#2a1410] font-bold text-sm mb-5 truncate">{{ stockForm.titlu }}</p>
        <div class="grid grid-cols-2 gap-4 mb-6">
          <div>
            <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-2">Stoc Total</label>
            <input v-model.number="stockForm.stoc_total" type="number" min="0" class="w-full px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-sans text-sm text-[#2a1410] focus:outline-none transition-colors">
          </div>
          <div>
            <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-2">Disponibil</label>
            <input v-model.number="stockForm.stoc_disponibil" type="number" min="0" class="w-full px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-sans text-sm text-[#2a1410] focus:outline-none transition-colors">
          </div>
        </div>
        <div v-if="stockMsg.error" class="mb-4 p-3 bg-[#ff3d5a]/5 border border-[#ff3d5a]/20 rounded-sm">
          <p class="text-[#ff3d5a] font-mono text-[10px] uppercase tracking-widest">{{ stockMsg.error }}</p>
        </div>
        <div v-if="stockMsg.success" class="mb-4 p-3 bg-[#2a5c3a]/5 border border-[#2a5c3a]/20 rounded-sm">
          <p class="text-[#2a5c3a] font-mono text-[10px] uppercase tracking-widest">{{ stockMsg.success }}</p>
        </div>
        <button @click="submitStock" class="w-full px-5 py-3 bg-[#c9a84c] text-dark hover:opacity-90 font-mono text-[10px] uppercase tracking-widest font-bold rounded-sm transition-all shadow-sm">
          Actualizează
        </button>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="deleteBookOpen" class="fixed inset-0 z-[60] flex items-center justify-center p-4" @click.self="deleteBookOpen = false">
      <div class="absolute inset-0 bg-dark/60 backdrop-blur-sm" @click="deleteBookOpen = false"></div>
      <div class="relative bg-white rounded-sm shadow-[0_4px_24px_rgba(42,20,16,0.1)] border border-[#2a1410]/10 w-full max-w-md z-10 p-6 sm:p-8 text-center">
        <div class="w-16 h-16 rounded-sm bg-[#ff3d5a]/10 border border-[#ff3d5a]/20 flex items-center justify-center mx-auto mb-5">
           <i class="pi pi-exclamation-triangle text-2xl text-[#ff3d5a]"></i>
        </div>
        <h2 class="text-lg font-bold font-display uppercase tracking-tight text-[#2a1410] mb-3">Șterge Cartea?</h2>
        <p class="text-[#7a5a55] font-serif italic text-sm mb-8">
          Ești sigur că vrei să ștergi <strong>{{ deleteTarget?.titlu }}</strong>? Această acțiune nu poate fi anulată.
        </p>
        <div v-if="deleteMsg.error" class="mb-5 p-3 bg-[#ff3d5a]/5 border border-[#ff3d5a]/20 rounded-sm">
          <p class="text-[#ff3d5a] font-mono text-[10px] uppercase tracking-widest">{{ deleteMsg.error }}</p>
        </div>
        <div class="flex flex-col sm:flex-row gap-3">
          <button @click="deleteBookOpen = false" class="flex-1 px-5 py-3 bg-white border border-[#2a1410]/20 text-[#2a1410] font-mono text-[10px] uppercase tracking-widest font-bold rounded-sm hover:bg-cream-dark transition-colors">
            Anulează
          </button>
          <button @click="submitDeleteBook" class="flex-1 px-5 py-3 bg-[#ff3d5a] hover:bg-[#ff3d5a]/90 text-white font-mono text-[10px] uppercase tracking-widest font-bold rounded-sm transition-colors">
            Șterge Definitiv
          </button>
        </div>
      </div>
    </div>

    <!-- Add Announcement Modal -->
    <div v-if="addAnuntOpen" class="fixed inset-0 z-[60] flex items-center justify-center p-4" @click.self="addAnuntOpen = false">
      <div class="absolute inset-0 bg-dark/60 backdrop-blur-sm" @click="addAnuntOpen = false"></div>
      <div class="relative bg-white rounded-sm shadow-[0_4px_24px_rgba(42,20,16,0.1)] border border-[#2a1410]/10 w-full max-w-lg z-10 p-6 sm:p-8 max-h-[90vh] overflow-y-auto custom-scrollbar">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-sm font-bold font-display uppercase tracking-tight text-[#2a1410]">Anunț Nou</h2>
          <button @click="addAnuntOpen = false" class="text-[#7a5a55] hover:text-[#2a1410] text-2xl font-bold leading-none">&times;</button>
        </div>
        <form @submit.prevent="submitAddAnunt" class="space-y-5">
          <div>
            <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-2">Titlu *</label>
            <input v-model="addAnuntForm.titlu" type="text" required maxlength="255" class="w-full px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-sans text-sm text-[#2a1410] focus:outline-none transition-colors">
          </div>
          <div>
            <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-2">Conținut *</label>
            <textarea v-model="addAnuntForm.anunt" required rows="6" class="w-full px-4 py-3 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-serif text-sm text-[#2a1410] focus:outline-none transition-colors resize-none"></textarea>
          </div>
          <div v-if="addAnuntMsg.error" class="p-3 bg-[#ff3d5a]/5 border border-[#ff3d5a]/20 rounded-sm">
            <p class="text-[#ff3d5a] font-mono text-[10px] uppercase tracking-widest">{{ addAnuntMsg.error }}</p>
          </div>
          <div v-if="addAnuntMsg.success" class="p-3 bg-[#2a5c3a]/5 border border-[#2a5c3a]/20 rounded-sm">
            <p class="text-[#2a5c3a] font-mono text-[10px] uppercase tracking-widest">{{ addAnuntMsg.success }}</p>
          </div>
          <button type="submit" class="w-full px-5 py-3 mt-4 bg-[#c9a84c] text-dark hover:opacity-90 font-mono text-[10px] uppercase tracking-widest font-bold rounded-sm transition-all shadow-sm">
            Publică Anunț
          </button>
        </form>
      </div>
    </div>

    <!-- Edit Announcement Modal -->
    <div v-if="editAnuntOpen" class="fixed inset-0 z-[60] flex items-center justify-center p-4" @click.self="editAnuntOpen = false">
      <div class="absolute inset-0 bg-dark/60 backdrop-blur-sm" @click="editAnuntOpen = false"></div>
      <div class="relative bg-white rounded-sm shadow-[0_4px_24px_rgba(42,20,16,0.1)] border border-[#2a1410]/10 w-full max-w-lg z-10 p-6 sm:p-8 max-h-[90vh] overflow-y-auto custom-scrollbar">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-sm font-bold font-display uppercase tracking-tight text-[#2a1410]">Editează Anunț</h2>
          <button @click="editAnuntOpen = false" class="text-[#7a5a55] hover:text-[#2a1410] text-2xl font-bold leading-none">&times;</button>
        </div>
        <form @submit.prevent="submitEditAnunt" class="space-y-5">
          <div>
            <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-2">Titlu</label>
            <input v-model="editAnuntForm.titlu" type="text" maxlength="255" class="w-full px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-sans text-sm text-[#2a1410] focus:outline-none transition-colors">
          </div>
          <div>
            <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-2">Conținut</label>
            <textarea v-model="editAnuntForm.anunt" rows="6" class="w-full px-4 py-3 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-serif text-sm text-[#2a1410] focus:outline-none transition-colors resize-none"></textarea>
          </div>
          <div v-if="editAnuntMsg.error" class="p-3 bg-[#ff3d5a]/5 border border-[#ff3d5a]/20 rounded-sm">
            <p class="text-[#ff3d5a] font-mono text-[10px] uppercase tracking-widest">{{ editAnuntMsg.error }}</p>
          </div>
          <div v-if="editAnuntMsg.success" class="p-3 bg-[#2a5c3a]/5 border border-[#2a5c3a]/20 rounded-sm">
            <p class="text-[#2a5c3a] font-mono text-[10px] uppercase tracking-widest">{{ editAnuntMsg.success }}</p>
          </div>
          <button type="submit" class="w-full px-5 py-3 mt-4 bg-[#c9a84c] text-dark hover:opacity-90 font-mono text-[10px] uppercase tracking-widest font-bold rounded-sm transition-all shadow-sm">
            Salvează Modificări
          </button>
        </form>
      </div>
    </div>

    <!-- Delete Announcement Modal -->
    <div v-if="deleteAnuntOpen" class="fixed inset-0 z-[60] flex items-center justify-center p-4" @click.self="deleteAnuntOpen = false">
      <div class="absolute inset-0 bg-dark/60 backdrop-blur-sm" @click="deleteAnuntOpen = false"></div>
      <div class="relative bg-white rounded-sm shadow-[0_4px_24px_rgba(42,20,16,0.1)] border border-[#2a1410]/10 w-full max-w-md z-10 p-6 sm:p-8 text-center">
        <div class="w-16 h-16 rounded-sm bg-[#ff3d5a]/10 border border-[#ff3d5a]/20 flex items-center justify-center mx-auto mb-5">
           <i class="pi pi-exclamation-triangle text-2xl text-[#ff3d5a]"></i>
        </div>
        <h2 class="text-lg font-bold font-display uppercase tracking-tight text-[#2a1410] mb-3">Șterge Anunțul?</h2>
        <p class="text-[#7a5a55] font-serif italic text-sm mb-8">
          Ești sigur că vrei să ștergi anunțul <strong>{{ deleteAnuntTarget?.titlu }}</strong>?
        </p>
        <div v-if="deleteAnuntMsg.error" class="mb-5 p-3 bg-[#ff3d5a]/5 border border-[#ff3d5a]/20 rounded-sm">
          <p class="text-[#ff3d5a] font-mono text-[10px] uppercase tracking-widest">{{ deleteAnuntMsg.error }}</p>
        </div>
        <div class="flex flex-col sm:flex-row gap-3">
          <button @click="deleteAnuntOpen = false" class="flex-1 px-5 py-3 bg-white border border-[#2a1410]/20 text-[#2a1410] font-mono text-[10px] uppercase tracking-widest font-bold rounded-sm hover:bg-cream-dark transition-colors">
            Anulează
          </button>
          <button @click="submitDeleteAnunt" class="flex-1 px-5 py-3 bg-[#ff3d5a] hover:bg-[#ff3d5a]/90 text-white font-mono text-[10px] uppercase tracking-widest font-bold rounded-sm transition-colors">
            Șterge Definitiv
          </button>
        </div>
      </div>
    </div>

    <!-- RETURNARE ÎMPRUMUT MODAL -->
    <div v-if="returnareModalOpen" class="fixed inset-0 z-[60] flex items-center justify-center p-4" @click.self="returnareModalOpen = false">
      <div class="absolute inset-0 bg-dark/60 backdrop-blur-sm" @click="returnareModalOpen = false"></div>
      <div class="relative bg-white rounded-sm shadow-[0_4px_24px_rgba(42,20,16,0.1)] border border-[#2a1410]/10 w-full max-w-sm z-10 p-6 sm:p-8">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-sm font-bold font-display uppercase tracking-tight text-[#2a1410]">Returnare Carte</h2>
          <button @click="returnareModalOpen = false" class="text-[#7a5a55] hover:text-[#2a1410] text-2xl font-bold leading-none">&times;</button>
        </div>
        <p class="text-[#2a1410] font-bold text-sm mb-1 truncate">{{ returnareTarget?.titlu }}</p>
        <p class="font-mono text-[10px] uppercase tracking-widest text-[#7a5a55] mb-6">de {{ returnareTarget?.autor }}</p>

        <!-- Modificare dată scadentă -->
        <div class="mb-5">
          <label class="block font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-2">Modifică data scadentă</label>
          <div class="grid grid-cols-2 gap-3 mb-3">
            <input v-model="returnareNovaDataDate" type="date" class="w-full px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-mono text-xs text-[#2a1410] focus:outline-none transition-colors">
            <input v-model="returnareNovaDataTime" type="time" class="w-full px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-mono text-xs text-[#2a1410] focus:outline-none transition-colors">
          </div>
          <button
            @click="prelungesteData"
            :disabled="salvandData || !returnareNovaDataDate || !returnareNovaDataTime"
            class="w-full px-5 py-3 bg-white border border-[#2a1410]/20 text-[#2a1410] hover:bg-cream-dark font-mono text-[10px] uppercase tracking-widest font-bold rounded-sm disabled:opacity-50 flex items-center justify-center gap-2 transition-colors"
          >
            <i :class="salvandData ? 'pi pi-spin pi-spinner' : 'pi pi-calendar'"></i>
            {{ salvandData ? 'Se salvează...' : 'Salvează data scadentă' }}
          </button>
        </div>

        <div class="border-t border-[#2a1410]/10 mb-6"></div>

        <div v-if="returnareMsg.error" class="mb-4 p-3 bg-[#ff3d5a]/5 border border-[#ff3d5a]/20 rounded-sm">
          <p class="text-[#ff3d5a] font-mono text-[10px] uppercase tracking-widest">{{ returnareMsg.error }}</p>
        </div>
        <div v-if="returnareMsg.success" class="mb-4 p-3 bg-[#2a5c3a]/5 border border-[#2a5c3a]/20 rounded-sm">
          <p class="text-[#2a5c3a] font-mono text-[10px] uppercase tracking-widest">{{ returnareMsg.success }}</p>
        </div>

        <button
          @click="returneazaAcum"
          :disabled="procesandReturnare"
          class="w-full px-5 py-3 bg-[#c9a84c] text-dark hover:opacity-90 font-mono text-[10px] uppercase tracking-widest font-bold rounded-sm disabled:opacity-50 flex items-center justify-center gap-2 transition-all shadow-sm"
        >
          <i :class="procesandReturnare ? 'pi pi-spin pi-spinner' : 'pi pi-check-circle'"></i>
          {{ procesandReturnare ? 'Se procesează...' : 'Returnează acum' }}
        </button>
      </div>
    </div>

    <!-- USERS LIST MODAL -->
    <div v-if="usersListOpen" class="fixed inset-0 z-[60] flex items-center justify-center p-4" @click.self="usersListOpen = false">
      <div class="absolute inset-0 bg-dark/60 backdrop-blur-sm" @click="usersListOpen = false"></div>
      <div class="relative bg-white rounded-sm shadow-[0_4px_24px_rgba(42,20,16,0.1)] border border-[#2a1410]/10 w-full max-w-2xl z-10 flex flex-col max-h-[90vh]">
        <!-- Header -->
        <div class="flex items-center justify-between p-6 sm:p-8 border-b border-[#2a1410]/10">
          <h2 class="text-sm font-bold font-display uppercase tracking-tight text-[#2a1410] flex items-center gap-2">
            <i class="pi pi-users text-[#c9a84c]"></i> Conturi Utilizatori
            <span class="font-mono text-[10px] text-[#7a5a55] ml-2">({{ filteredUsers.length }})</span>
          </h2>
          <button @click="usersListOpen = false" class="text-[#7a5a55] hover:text-[#2a1410] text-2xl font-bold leading-none transition-colors">&times;</button>
        </div>
        <!-- Search -->
        <div class="px-6 sm:px-8 py-5 border-b border-[#2a1410]/5 bg-cream/30">
          <input
            v-model="usersSearch"
            type="text"
            placeholder="Caută după nume sau email..."
            class="w-full px-4 py-2.5 bg-white border border-[#2a1410]/20 focus:border-[#c9a84c] rounded-sm font-sans text-sm text-[#2a1410] placeholder-[#7a5a55]/50 focus:outline-none transition-colors"
          >
        </div>
        <!-- List -->
        <div class="overflow-y-auto flex-1 p-6 sm:p-8 custom-scrollbar">
          <div v-if="loadingUsers" class="flex items-center justify-center py-12">
            <i class="pi pi-spin pi-spinner text-2xl text-[#c9a84c]"></i>
          </div>
          <div v-else-if="filteredUsers.length === 0" class="text-center py-12 text-[#7a5a55] font-serif italic text-sm">
            <i class="pi pi-users text-3xl mb-3 block opacity-20"></i>
            Niciun utilizator găsit.
          </div>
          <div v-else class="space-y-3">
            <div
              v-for="u in filteredUsers"
              :key="u.user_id"
              @click="openUserDetail(u)"
              class="flex items-center gap-4 p-4 rounded-sm border border-[#2a1410]/10 bg-white hover:border-[#c9a84c]/50 hover:bg-cream cursor-pointer transition-all group"
            >
              <div class="w-10 h-10 rounded-sm bg-cream-dark flex items-center justify-center shrink-0 border border-[#2a1410]/10">
                <i class="pi pi-user text-[#7a5a55] group-hover:text-[#c9a84c] transition-colors"></i>
              </div>
              <div class="flex-1 min-w-0">
                <p class="font-bold text-[#2a1410] text-sm truncate">{{ u.username }}</p>
                <p class="text-[#7a5a55] font-serif italic text-xs truncate">{{ u.email }}</p>
              </div>
              <span :class="u.rol === 'bibliotecar' ? 'bg-[#c9a84c] text-dark' : 'bg-cream-dark text-[#7a5a55] border border-[#2a1410]/10'" class="font-mono text-[9px] uppercase tracking-widest font-bold px-2 py-1 rounded-sm shrink-0">
                {{ u.rol === 'bibliotecar' ? 'Bibliotecar' : 'Elev' }}
              </span>
              <i class="pi pi-chevron-right text-[#7a5a55]/40 group-hover:text-[#c9a84c] text-sm shrink-0 transition-colors"></i>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- USER DETAIL MODAL -->
    <div v-if="userDetailOpen" class="fixed inset-0 z-[70] flex items-center justify-center p-4" @click.self="userDetailOpen = false">
      <div class="absolute inset-0 bg-dark/60 backdrop-blur-sm" @click="userDetailOpen = false"></div>
      <div class="relative bg-white rounded-sm shadow-[0_4px_24px_rgba(42,20,16,0.1)] border border-[#2a1410]/10 w-full max-w-2xl z-10 flex flex-col max-h-[90vh]">
        <!-- Header -->
        <div class="flex items-center justify-between p-6 sm:p-8 border-b border-[#2a1410]/10">
          <h2 class="text-sm font-bold font-display uppercase tracking-tight text-[#2a1410] flex items-center gap-2">
            <i class="pi pi-user text-[#c9a84c]"></i>
            {{ userDetail ? userDetail.user.username : 'Detalii Cont' }}
          </h2>
          <button @click="userDetailOpen = false" class="text-[#7a5a55] hover:text-[#2a1410] text-2xl font-bold leading-none transition-colors">&times;</button>
        </div>

        <!-- Loading -->
        <div v-if="loadingUserDetail" class="flex items-center justify-center py-16">
          <i class="pi pi-spin pi-spinner text-2xl text-[#c9a84c]"></i>
        </div>

        <!-- Content -->
        <div v-else-if="userDetail" class="overflow-y-auto flex-1 p-6 sm:p-8 space-y-8 custom-scrollbar">

          <!-- Profile Info -->
          <div class="flex items-center gap-5 p-5 bg-cream rounded-sm border border-[#2a1410]/10">
            <img
              :src="`/api/auth/profile-picture/${encodeURIComponent(userDetail.user.username)}?t=${Date.now()}`"
              class="w-16 h-16 rounded-sm object-cover border border-[#2a1410]/20"
              @error="$event.target.src='/api/auth/profile-picture/default'"
            >
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-3 flex-wrap mb-1">
                <p class="font-bold text-[#2a1410] text-lg">{{ userDetail.user.username }}</p>
                <span :class="userDetail.user.rol === 'bibliotecar' ? 'bg-[#c9a84c] text-dark' : 'bg-white text-[#7a5a55] border border-[#2a1410]/10'" class="font-mono text-[9px] uppercase tracking-widest font-bold px-2 py-1 rounded-sm">
                  {{ userDetail.user.rol === 'bibliotecar' ? 'Bibliotecar' : 'Elev' }}
                </span>
              </div>
              <p class="text-[#7a5a55] font-serif italic text-sm">{{ userDetail.user.email }}</p>
              <p v-if="userDetail.user.telefon" class="text-[#7a5a55] font-mono text-[10px] uppercase tracking-widest mt-2"><i class="pi pi-phone mr-1"></i>{{ userDetail.user.telefon }}</p>
            </div>
          </div>

          <p v-if="userDetail.user.description" class="text-[#3b2b18] font-serif italic text-sm border-l-2 border-[#c9a84c] pl-4">
            „{{ userDetail.user.description }}"
          </p>

          <!-- Stats row -->
          <div class="grid grid-cols-3 gap-4 text-center">
            <div class="bg-white border border-[#2a1410]/10 rounded-sm p-4">
              <p class="text-2xl font-bold font-display text-[#2a1410]">{{ userDetail.books_borrowed.length }}</p>
              <p class="font-mono text-[9px] uppercase tracking-widest text-[#7a5a55] mt-1">Împrumutate</p>
            </div>
            <div class="bg-white border border-[#2a1410]/10 rounded-sm p-4">
              <p class="text-2xl font-bold font-display text-[#2a1410]">{{ userDetail.books_read.length }}</p>
              <p class="font-mono text-[9px] uppercase tracking-widest text-[#7a5a55] mt-1">Citite</p>
            </div>
            <div class="bg-white border border-[#2a1410]/10 rounded-sm p-4">
              <p class="text-2xl font-bold font-display text-[#2a1410]">{{ userDetail.reviews.length }}</p>
              <p class="font-mono text-[9px] uppercase tracking-widest text-[#7a5a55] mt-1">Recenzii</p>
            </div>
          </div>

          <!-- Currently Borrowed -->
          <div>
            <h3 class="font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-4 pb-2 border-b border-[#2a1410]/10 flex items-center gap-2">
              <i class="pi pi-book"></i> Cărți Împrumutate Curent
            </h3>
            <div v-if="userDetail.books_borrowed.length === 0" class="text-[#7a5a55] font-serif italic text-sm py-2">Nicio carte împrumutată momentan.</div>
            <div v-else class="space-y-3">
              <div v-for="b in userDetail.books_borrowed" :key="b.carte_id" class="flex items-center gap-4 p-4 border border-[#2a5c3a]/20 bg-[#2a5c3a]/5 rounded-sm">
                <i class="pi pi-book text-[#2a5c3a] shrink-0"></i>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-bold text-[#2a1410] truncate">{{ b.titlu }}</p>
                  <p class="font-mono text-[10px] uppercase tracking-widest text-[#7a5a55] mt-1">{{ b.autor }} · ISBN: {{ b.ISBN }}</p>
                </div>
                <span class="font-mono text-[10px] text-[#2a5c3a] font-bold shrink-0">{{ formatDate(b.borrowed_at) }}</span>
              </div>
            </div>
          </div>

          <!-- Books Read -->
          <div>
            <h3 class="font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-4 pb-2 border-b border-[#2a1410]/10 flex items-center gap-2">
              <i class="pi pi-check-circle"></i> Cărți Citite / Returnate
            </h3>
            <div v-if="userDetail.books_read.length === 0" class="text-[#7a5a55] font-serif italic text-sm py-2">Nicio carte returnată înregistrată.</div>
            <div v-else class="space-y-3">
              <div v-for="b in userDetail.books_read" :key="b.carte_id" class="flex items-center gap-4 p-4 border border-[#2a1410]/10 bg-white rounded-sm">
                <i class="pi pi-check text-[#7a5a55] shrink-0"></i>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-bold text-[#2a1410] truncate">{{ b.titlu }}</p>
                  <p class="font-mono text-[10px] uppercase tracking-widest text-[#7a5a55] mt-1">{{ b.autor }} · ISBN: {{ b.ISBN }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Borrow History -->
          <div>
            <h3 class="font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-4 pb-2 border-b border-[#2a1410]/10 flex items-center gap-2">
              <i class="pi pi-history"></i> Istoric Cereri Împrumut
            </h3>
            <div v-if="userDetail.borrow_history.length === 0" class="text-[#7a5a55] font-serif italic text-sm py-2">Nicio cerere înregistrată.</div>
            <div v-else class="space-y-3">
              <div v-for="r in userDetail.borrow_history" :key="r.cerere_id" class="flex items-center gap-4 p-4 border border-[#2a1410]/10 bg-white rounded-sm">
                <span :class="[
                  'font-mono text-[9px] uppercase tracking-widest font-bold px-2 py-1 rounded-sm shrink-0 border',
                  r.status === 'pending' ? 'bg-amber-50 text-amber-700 border-amber-200' :
                  r.status === 'approved' ? 'bg-[#2a5c3a]/10 text-[#2a5c3a] border-[#2a5c3a]/20' :
                  'bg-[#ff3d5a]/10 text-[#ff3d5a] border-[#ff3d5a]/20'
                ]">
                  {{ r.status === 'pending' ? 'Așteptare' : r.status === 'approved' ? 'Aprobat' : 'Respins' }}
                </span>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-bold text-[#2a1410] truncate">{{ r.titlu }}</p>
                  <p class="font-mono text-[10px] uppercase tracking-widest text-[#7a5a55] mt-1">{{ r.autor }}</p>
                </div>
                <span class="font-mono text-[10px] text-[#7a5a55] shrink-0">{{ formatDate(r.created_at) }}</span>
              </div>
            </div>
          </div>

          <!-- Reviews -->
          <div>
            <h3 class="font-mono text-[10px] uppercase tracking-widest font-bold text-[#7a5a55] mb-4 pb-2 border-b border-[#2a1410]/10 flex items-center gap-2">
              <i class="pi pi-star"></i> Recenzii
            </h3>
            <div v-if="userDetail.reviews.length === 0" class="text-[#7a5a55] font-serif italic text-sm py-2">Nicio recenzie scrisă.</div>
            <div v-else class="space-y-4">
              <div v-for="r in userDetail.reviews" :key="r.id" class="p-5 border border-[#2a1410]/10 bg-cream rounded-sm">
                <div class="flex items-start justify-between gap-4 mb-2">
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-bold text-[#2a1410] truncate">{{ r.titlu }}</p>
                    <p class="font-mono text-[10px] uppercase tracking-widest text-[#7a5a55] mt-1">{{ r.autor }}</p>
                  </div>
                  <div class="flex items-center gap-0.5 shrink-0">
                    <span v-for="star in 5" :key="star" :class="star <= r.nota ? 'text-[#c9a84c]' : 'text-[#2a1410]/20'" class="text-sm">★</span>
                  </div>
                </div>
                <p class="text-[#3b2b18] font-serif italic text-sm leading-relaxed mt-3 border-l-2 border-[#2a1410]/10 pl-3">{{ r.comentariu }}</p>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Profile',
  data() {
    return {
      // admin tabs
      activeTab: 'cereri',

      // profilul utilizatorului
      user: {
        name: '',
        profilePicture: '/api/auth/profile-picture/default',
        joinDate: 'Ianuarie 2023',
        description: null,
        totalBooksRead: 0,
        booksRead: [],
        userReviews: []
      },
      isBibliotecar: false,
      loadingReviews: false,
      // AI recommendations
      aiRecommendations: '',
      loadingAi: false,
      aiError: '',
      // Edit profile
      editProfileOpen: false,
      editDescription: '',
      profileMsg: { error: '', success: '' },
      savingDescription: false,
      // panoul bibliotecarului
      bookRequests: [],
      loadingRequests: false,
      requestFilter: 'pending',
      downloadingReport: false,
      // Pickup interval modal
      pickupModalOpen: false,
      pickupReq: {},
      pickupFromDate: '',
      pickupFromTime: '08:00',
      pickupUntilDate: '',
      pickupUntilTime: '14:00',
      pickupError: '',
      approvingRequest: false,
      allBooks: [],
      filteredLibBooks: [],
      libSearch: '',
      loadingBooks: false,
      imageCacheBust: Date.now(),
      bookImageCarteId: null,
      bookPdfCarteId: null,
      // Invitații club
      inviteExpiry: 24,
      inviteOptions: [
        { label: '1 oră', value: 1 },
        { label: '24 ore', value: 24 },
        { label: '7 zile', value: 168 }
      ],
      inviteLoading: false,
      generatedInviteLink: '',
      inviteExpiresAt: '',
      inviteCopied: false,
      inviteError: '',
      inviteExpiry: 1, // days
      
      pendingThreads: [],
      pendingThreadsLoading: false,     // Add book
      addBookOpen: false,
      addForm: { titlu: '', autor: '', ISBN: '', gen: '', stoc_total: 1, stoc_disponibil: 1, pozitie: '', cod: '' },
      addMsg: { error: '', success: '' },
      // Edit book
      editBookOpen: false,
      editBookForm: { carte_id: null, titlu: '', autor: '', ISBN: '', gen: '', stoc_total: 0, stoc_disponibil: 0, pozitie: '', cod: '' },
      editBookMsg: { error: '', success: '' },
      // Stock quick-edit
      stockModalOpen: false,
      stockForm: { carte_id: null, titlu: '', stoc_total: 0, stoc_disponibil: 0 },
      stockMsg: { error: '', success: '' },
      // Delete book
      deleteBookOpen: false,
      deleteTarget: null,
      deleteMsg: { error: '' },
      // anunțuri
      allAnunturi: [],
      loadingAnunturi: false,
      // Add announcement
      addAnuntOpen: false,
      addAnuntForm: { titlu: '', anunt: '' },
      addAnuntMsg: { error: '', success: '' },
      // Edit announcement
      editAnuntOpen: false,
      editAnuntForm: { anunt_id: null, titlu: '', anunt: '' },
      editAnuntMsg: { error: '', success: '' },
      // Delete announcement
      deleteAnuntOpen: false,
      deleteAnuntTarget: null,
      deleteAnuntMsg: { error: '' },
      // lista utilizatorilor (bibliotecar)
      usersListOpen: false,
      allUsers: [],
      loadingUsers: false,
      usersSearch: '',
      // User detail modal
      userDetailOpen: false,
      loadingUserDetail: false,
      userDetail: null,
      // gestionare elevi (panoul nou)
      eleviLista: [],
      loadingElevi: false,
      eleviSearch: '',
      elevSelectat: null,
      elevDetalii: null,
      loadingElevDetalii: false,
      confirmandRidicare: null,
      // Returnare împrumut
      returnareModalOpen: false,
      returnareTarget: null,
      returnareNovaDataDate: '',
      returnareNovaDataTime: '',
      returnareMsg: { error: '', success: '' },
      procesandReturnare: false,
      salvandData: false
    }
  },
  computed: {
    pendingRequestsCount() {
      return this.bookRequests.filter(r => r.status === 'pending').length
    },
    approvedWaitingCount() {
      return this.bookRequests.filter(r => r.status === 'approved').length
    },
    filteredUsers() {
      if (!this.usersSearch.trim()) return this.allUsers
      const q = this.usersSearch.toLowerCase()
      return this.allUsers.filter(u =>
        u.username.toLowerCase().includes(q) ||
        u.email.toLowerCase().includes(q)
      )
    },
    eleviFiltrati() {
      if (!this.eleviSearch.trim()) return this.eleviLista
      const q = this.eleviSearch.toLowerCase()
      return this.eleviLista.filter(u =>
        u.username.toLowerCase().includes(q) ||
        u.email.toLowerCase().includes(q)
      )
    },
    aprovateAsteptare() {
      if (!this.elevDetalii) return []
      return this.elevDetalii.borrow_history.filter(r => r.status === 'approved')
    }
  },
  mounted() {
    this.loadProfile()
  },
  methods: {
    changeTab(tabKey) {
      this.activeTab = tabKey
      if (tabKey === 'club') {
        this.fetchPendingThreads()
      }
    },
    // metode profil
    openProfileEditModal() {
      this.editDescription = this.user.description || ''
      this.profileMsg = { error: '', success: '' }
      this.editProfileOpen = true
    },
    triggerFileInput() {
      this.$refs.fileInput.click()
    },
    async uploadProfilePicture(event) {
      const file = event.target.files[0]
      if (!file) return
      const formData = new FormData()
      formData.append('file', file)
      try {
        const response = await fetch('/api/auth/profile-picture', {
          method: 'POST',
          credentials: 'include',
          body: formData
        })
        if (response.ok) {
          this.loadProfilePicture(this.user.name)
        }
      } catch (error) {
        console.error('Upload error:', error)
      }
      this.$refs.fileInput.value = ''
    },
    loadProfilePicture(username) {
      if (!username) return
      this.user.profilePicture = `/api/auth/profile-picture/${encodeURIComponent(username)}?t=${Date.now()}`
    },
    async saveDescription() {
      this.savingDescription = true
      this.profileMsg = { error: '', success: '' }
      try {
        const response = await fetch('/api/auth/profile', {
          method: 'PUT',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ description: this.editDescription })
        })
        const data = await response.json()
        if (!response.ok) {
          this.profileMsg.error = data.message || 'Nu s-a putut actualiza descrierea.'
          return
        }
        this.user.description = this.editDescription || null
        this.profileMsg.success = 'Descriere actualizată cu succes!'
        setTimeout(() => { this.editProfileOpen = false }, 1200)
      } catch {
        this.profileMsg.error = 'Eroare de rețea. Încearcă din nou.'
      } finally {
        this.savingDescription = false
      }
    },
    async loadProfile() {
      try {
        const response = await fetch('/api/auth/profile', { credentials: 'include' })
        const data = await response.json()
        if (!response.ok) {
          this.$router.push('/login')
          return
        }
        this.user.name = data.username || ''
        this.user.description = data.description || null
        this.loadProfilePicture(data.username)

        // Verificăm rolul
        const meRes = await fetch('/api/auth/me', { credentials: 'include' })
        if (meRes.ok) {
          const me = await meRes.json()
          this.isBibliotecar = me.rol === 'bibliotecar'
        }

        if (data.user_id) {
          this.loadBooksRead()
          this.loadUserReviews()
        }

        // Încărcăm datele panoului bibliotecarului
        if (this.isBibliotecar) {
          this.fetchBookRequests()
          this.fetchAllBooks()
          this.fetchAllAnunturi()
          this.fetchEleviLista()
        }
      } catch (error) {
        console.error('Profile fetch error:', error)
        this.$router.push('/login')
      }
    },
    async loadBooksRead() {
      try {
        const response = await fetch('/api/auth/books-read', { credentials: 'include' })
        const data = await response.json()
        if (response.ok && data.books) {
          this.user.booksRead = data.books
          this.user.totalBooksRead = data.books.length
        }
      } catch (error) {
        console.error('Books read fetch error:', error)
      }
    },
    async loadUserReviews() {
      this.loadingReviews = true
      try {
        const response = await fetch('/api/reviews/user', { credentials: 'include' })
        const data = await response.json()
        if (response.ok && data.reviews) {
          this.user.userReviews = data.reviews
        }
      } catch (error) {
        console.error('User reviews fetch error:', error)
      } finally {
        this.loadingReviews = false
      }
    },

    // metode bibliotecar

    async downloadReport() {
      this.downloadingReport = true
      try {
        const res = await fetch('/api/librarian/report/docx')
        if (!res.ok) throw new Error('Server error')
        const blob = await res.blob()
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        const now = new Date()
        const stamp = `${now.getFullYear()}${String(now.getMonth()+1).padStart(2,'0')}${String(now.getDate()).padStart(2,'0')}`
        a.href = url
        a.download = `raport_biblioteca_${stamp}.docx`
        document.body.appendChild(a)
        a.click()
        a.remove()
        URL.revokeObjectURL(url)
      } catch (e) {
        alert('Nu s-a putut genera raportul. Încearcă din nou.')
      } finally {
        this.downloadingReport = false
      }
    },

    // recomandări ai
    async loadAiRecommendations() {
      this.loadingAi = true
      this.aiError = ''
      this.aiRecommendations = ''
      try {
        const res = await fetch('/api/ai/recommend', { credentials: 'include' })
        const data = await res.json()
        if (data.success) {
          if (data.no_history) {
            this.aiRecommendations = 'Nu ai nicio carte citită încă. Încearcă să citești câteva cărți și revin cu recomandări personalizate!'
          } else {
            this.aiRecommendations = data.recommendations
          }
        } else {
          this.aiError = data.message || 'Eroare la generarea recomandărilor.'
        }
      } catch {
        this.aiError = 'Eroare de rețea. Încearcă din nou.'
      } finally {
        this.loadingAi = false
      }
    },

    // cereri de împrumut
    async fetchBookRequests() {
      this.loadingRequests = true
      try {
        const qs = this.requestFilter !== 'all' ? `?status=${this.requestFilter}` : ''
        const res = await fetch(`/api/book-requests${qs}`, { credentials: 'include' })
        const data = await res.json()
        if (data.success) {
          this.bookRequests = data.cereri
        }
      } catch (error) {
        console.error('Error fetching book requests:', error)
      } finally {
        this.loadingRequests = false
      }
    },
    openPickupModal(req) {
      this.pickupReq = req
      this.pickupError = ''
      // Implicit: azi la 08:00 → azi la 14:00
      const now = new Date()
      const pad = n => String(n).padStart(2, '0')
      const dateStr = `${now.getFullYear()}-${pad(now.getMonth()+1)}-${pad(now.getDate())}`
      this.pickupFromDate = dateStr
      this.pickupFromTime = '08:00'
      this.pickupUntilDate = dateStr
      this.pickupUntilTime = '14:00'
      this.pickupModalOpen = true
    },
    // Auto-inserează ':' după primele 2 cifre pentru câmpurile de oră HH:MM
    formatTimeInput(field, event) {
      let val = event.target.value.replace(/\D/g, '')
      if (val.length >= 3) val = val.slice(0, 2) + ':' + val.slice(2, 4)
      else if (val.length === 2 && !event.target.value.includes(':')) val = val + ':'
      this[field] = val
    },

    async confirmApprove() {
      this.pickupError = ''
      const timeRe = /^([01]\d|2[0-3]):[0-5]\d$/
      if (!this.pickupFromDate || !timeRe.test(this.pickupFromTime) || !this.pickupUntilDate || !timeRe.test(this.pickupUntilTime)) {
        this.pickupError = 'Completează toate câmpurile. Ora trebuie să fie în format HH:MM (ex: 08:30).'
        return
      }
      const isoFrom  = `${this.pickupFromDate}T${this.pickupFromTime}`
      const isoUntil = `${this.pickupUntilDate}T${this.pickupUntilTime}`
      if (isoFrom >= isoUntil) {
        this.pickupError = 'Data de start trebuie să fie înainte de data de final.'
        return
      }
      this.approvingRequest = true
      try {
        const res = await fetch(`/api/book-requests/${this.pickupReq.cerere_id}`, {
          method: 'PUT',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            status: 'approved',
            ridicare_de_la: isoFrom,
            ridicare_pana_la: isoUntil
          })
        })
        if (res.ok) {
          this.pickupModalOpen = false
          await this.fetchBookRequests()
        } else {
          const d = await res.json().catch(() => ({}))
          this.pickupError = d.message || 'Eroare la aprobare.'
        }
      } catch (e) {
        this.pickupError = 'Eroare de rețea.'
      } finally {
        this.approvingRequest = false
      }
    },

    async handleRequest(cerereId, status) {
      try {
        const res = await fetch(`/api/book-requests/${cerereId}`, {
          method: 'PUT',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ status })
        })
        if (res.ok) {
          await this.fetchBookRequests()
        }
      } catch (error) {
        console.error('Error updating request:', error)
      }
    },
    formatDate(isoStr) {
      if (!isoStr) return ''
      const d = new Date(isoStr)
      return d.toLocaleDateString('ro-RO', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
    },

    // cărți
    async fetchAllBooks() {
      this.loadingBooks = true
      try {
        const response = await fetch('/api/books')
        const data = await response.json()
        if (data.books) {
          this.allBooks = data.books
          this.filterLibBooks()
        }
      } catch (error) {
        console.error('Error fetching books:', error)
      } finally {
        this.loadingBooks = false
      }
    },
    filterLibBooks() {
      if (!this.libSearch.trim()) {
        this.filteredLibBooks = this.allBooks
        return
      }
      const q = this.libSearch.toLowerCase()
      this.filteredLibBooks = this.allBooks.filter(b =>
        b.titlu.toLowerCase().includes(q) ||
        b.autor.toLowerCase().includes(q) ||
        b.ISBN.toLowerCase().includes(q) ||
        b.gen.toLowerCase().includes(q)
      )
    },

    // adăugare carte
    openAddBookModal() {
      this.addForm = { titlu: '', autor: '', ISBN: '', gen: '', stoc_total: 1, stoc_disponibil: 1, pozitie: '', cod: '' }
      this.addMsg = { error: '', success: '' }
      this.addBookOpen = true
    },
    async submitAddBook() {
      this.addMsg = { error: '', success: '' }
      try {
        const res = await fetch('/api/books', {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.addForm)
        })
        const data = await res.json()
        if (res.ok) {
          this.addMsg.success = 'Carte adăugată cu succes!'
          await this.fetchAllBooks()
          setTimeout(() => { this.addBookOpen = false }, 1200)
        } else {
          this.addMsg.error = data.message || 'Eroare la adăugare'
        }
      } catch {
        this.addMsg.error = 'Eroare de rețea.'
      }
    },

    // editare carte
    openEditBookModal(book) {
      this.editBookForm = {
        carte_id: book.carte_id,
        titlu: book.titlu,
        autor: book.autor,
        ISBN: book.ISBN,
        gen: book.gen,
        stoc_total: book.stoc_total,
        stoc_disponibil: book.stoc_disponibil,
        pozitie: book.pozitie || '',
        cod: book.cod || ''
      }
      this.editBookMsg = { error: '', success: '' }
      this.editBookOpen = true
    },
    async submitEditBook() {
      this.editBookMsg = { error: '', success: '' }
      const { carte_id, ...fields } = this.editBookForm
      try {
        const res = await fetch(`/api/books/${carte_id}`, {
          method: 'PUT',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(fields)
        })
        const data = await res.json()
        if (res.ok) {
          this.editBookMsg.success = 'Carte actualizată cu succes!'
          await this.fetchAllBooks()
          setTimeout(() => { this.editBookOpen = false }, 1200)
        } else {
          this.editBookMsg.error = data.message || 'Eroare la actualizare'
        }
      } catch {
        this.editBookMsg.error = 'Eroare de rețea.'
      }
    },

    // actualizare rapidă stoc
    openStockModal(book) {
      this.stockForm = {
        carte_id: book.carte_id,
        titlu: book.titlu,
        stoc_total: book.stoc_total,
        stoc_disponibil: book.stoc_disponibil
      }
      this.stockMsg = { error: '', success: '' }
      this.stockModalOpen = true
    },
    async submitStock() {
      this.stockMsg = { error: '', success: '' }
      try {
        const res = await fetch(`/api/books/${this.stockForm.carte_id}`, {
          method: 'PUT',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            stoc_total: this.stockForm.stoc_total,
            stoc_disponibil: this.stockForm.stoc_disponibil
          })
        })
        const data = await res.json()
        if (res.ok) {
          this.stockMsg.success = 'Stoc actualizat!'
          await this.fetchAllBooks()
          setTimeout(() => { this.stockModalOpen = false }, 1000)
        } else {
          this.stockMsg.error = data.message || 'Eroare'
        }
      } catch {
        this.stockMsg.error = 'Eroare de rețea.'
      }
    },

    // ștergere carte
    confirmDeleteBook(book) {
      this.deleteTarget = book
      this.deleteMsg = { error: '' }
      this.deleteBookOpen = true
    },
    async submitDeleteBook() {
      this.deleteMsg = { error: '' }
      try {
        const res = await fetch(`/api/books/${this.deleteTarget.carte_id}`, {
          method: 'DELETE',
          credentials: 'include'
        })
        const data = await res.json()
        if (res.ok) {
          this.deleteBookOpen = false
          await this.fetchAllBooks()
        } else {
          this.deleteMsg.error = data.message || 'Eroare la ștergere'
        }
      } catch {
        this.deleteMsg.error = 'Eroare de rețea.'
      }
    },

    // încărcare copertă carte
    triggerBookImageInput(carteId) {
      this.bookImageCarteId = carteId
      this.$refs.bookImageInput.click()
    },
    async uploadBookImage(event) {
      const file = event.target.files[0]
      if (!file || !this.bookImageCarteId) return
      const formData = new FormData()
      formData.append('file', file)
      formData.append('carte_id', this.bookImageCarteId)
      try {
        const res = await fetch('/api/books/image', {
          method: 'POST',
          credentials: 'include',
          body: formData
        })
        if (res.ok) {
          this.imageCacheBust = Date.now()
        }
      } catch (error) {
        console.error('Book image upload error:', error)
      }
      this.$refs.bookImageInput.value = ''
      this.bookImageCarteId = null
    },
    triggerBookPdfInput(carteId) {
      this.bookPdfCarteId = carteId
      this.$refs.bookPdfInput.click()
    },
    async uploadBookPdf(event) {
      const file = event.target.files[0]
      if (!file || !this.bookPdfCarteId) return
      const formData = new FormData()
      formData.append('file', file)
      formData.append('carte_id', this.bookPdfCarteId)
      try {
        const res = await fetch('/api/books/pdf', {
          method: 'POST',
          credentials: 'include',
          body: formData
        })
        if (res.ok) {
          const book = this.libBooks.find(b => b.carte_id === this.bookPdfCarteId)
          if (book) book.has_pdf = true
          const fbook = this.filteredLibBooks.find(b => b.carte_id === this.bookPdfCarteId)
          if (fbook) fbook.has_pdf = true
        }
      } catch (error) {
        console.error('PDF upload error:', error)
      }
      this.$refs.bookPdfInput.value = ''
      this.bookPdfCarteId = null
    },
    async deleteBookPdf(book) {
      if (!confirm(`Ștergi PDF-ul pentru „${book.titlu}"?`)) return
      try {
        const res = await fetch(`/api/books/pdf/${book.carte_id}`, {
          method: 'DELETE',
          credentials: 'include'
        })
        if (res.ok) {
          book.has_pdf = false
        }
      } catch (error) {
        console.error('PDF delete error:', error)
      }
    },
    openPdfInTab(carteId) {
      window.open(`/api/books/pdf/${carteId}`, '_blank')
    },

    // metode anunțuri
    async fetchAllAnunturi() {
      this.loadingAnunturi = true
      try {
        const res = await fetch('/api/anunturi', { credentials: 'include' })
        const data = await res.json()
        if (data.success) {
          this.allAnunturi = data.anunturi
        }
      } catch (error) {
        console.error('Error fetching announcements:', error)
      } finally {
        this.loadingAnunturi = false
      }
    },

    // adăugare anunț
    openAddAnuntModal() {
      this.addAnuntForm = { titlu: '', anunt: '' }
      this.addAnuntMsg = { error: '', success: '' }
      this.addAnuntOpen = true
    },
    async submitAddAnunt() {
      this.addAnuntMsg = { error: '', success: '' }
      try {
        const res = await fetch('/api/anunturi', {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.addAnuntForm)
        })
        const data = await res.json()
        if (res.ok) {
          this.addAnuntMsg.success = 'Anunț publicat cu succes!'
          await this.fetchAllAnunturi()
          setTimeout(() => { this.addAnuntOpen = false }, 1200)
        } else {
          this.addAnuntMsg.error = data.message || 'Eroare la publicare'
        }
      } catch {
        this.addAnuntMsg.error = 'Eroare de rețea.'
      }
    },

    // editare anunț
    openEditAnuntModal(a) {
      this.editAnuntForm = {
        anunt_id: a.anunt_id,
        titlu: a.titlu,
        anunt: a.anunt
      }
      this.editAnuntMsg = { error: '', success: '' }
      this.editAnuntOpen = true
    },
    async submitEditAnunt() {
      this.editAnuntMsg = { error: '', success: '' }
      const { anunt_id, ...fields } = this.editAnuntForm
      try {
        const res = await fetch(`/api/anunturi/${anunt_id}`, {
          method: 'PUT',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(fields)
        })
        const data = await res.json()
        if (res.ok) {
          this.editAnuntMsg.success = 'Anunț actualizat cu succes!'
          await this.fetchAllAnunturi()
          setTimeout(() => { this.editAnuntOpen = false }, 1200)
        } else {
          this.editAnuntMsg.error = data.message || 'Eroare la actualizare'
        }
      } catch {
        this.editAnuntMsg.error = 'Eroare de rețea.'
      }
    },

    // ștergere anunț
    confirmDeleteAnunt(a) {
      this.deleteAnuntTarget = a
      this.deleteAnuntMsg = { error: '' }
      this.deleteAnuntOpen = true
    },
    async submitDeleteAnunt() {
      this.deleteAnuntMsg = { error: '' }
      try {
        const res = await fetch(`/api/anunturi/${this.deleteAnuntTarget.anunt_id}`, {
          method: 'DELETE',
          credentials: 'include'
        })
        const data = await res.json()
        if (res.ok) {
          this.deleteAnuntOpen = false
          await this.fetchAllAnunturi()
        } else {
          this.deleteAnuntMsg.error = data.message || 'Eroare la ștergere'
        }
      } catch {
        this.deleteAnuntMsg.error = 'Eroare de rețea.'
      }
    },

    // metode conturi utilizatori
    async openUsersListModal() {
      this.usersSearch = ''
      this.usersListOpen = true
      this.loadingUsers = true
      try {
        const res = await fetch('/api/admin/users', { credentials: 'include' })
        const data = await res.json()
        if (data.success) {
          this.allUsers = data.users
        }
      } catch (error) {
        console.error('Error fetching users:', error)
      } finally {
        this.loadingUsers = false
      }
    },
    async openUserDetail(user) {
      this.userDetail = null
      this.userDetailOpen = true
      this.loadingUserDetail = true
      try {
        const res = await fetch(`/api/admin/users/${user.user_id}`, { credentials: 'include' })
        const data = await res.json()
        if (data.success) {
          this.userDetail = data
        }
      } catch (error) {
        console.error('Error fetching user detail:', error)
      } finally {
        this.loadingUserDetail = false
      }
    },

    // metode gestionare elevi (panou nou)
    async fetchEleviLista() {
      this.loadingElevi = true
      try {
        const res = await fetch('/api/admin/users', { credentials: 'include' })
        const data = await res.json()
        if (data.success) {
          // Excludem bibliotecaristul din lista de elevi
          this.eleviLista = data.users.filter(u => u.rol !== 'bibliotecar')
        }
      } catch { /* ignorăm */ } finally {
        this.loadingElevi = false
      }
    },
    async selecteazaElev(u) {
      this.elevSelectat = u
      this.elevDetalii = null
      this.loadingElevDetalii = true
      try {
        const res = await fetch(`/api/admin/users/${u.user_id}`, { credentials: 'include' })
        const data = await res.json()
        if (data.success) this.elevDetalii = data
      } catch { /* ignorăm */ } finally {
        this.loadingElevDetalii = false
      }
    },
    async confirmaRidicare(cerereId) {
      this.confirmandRidicare = cerereId
      try {
        const res = await fetch(`/api/book-requests/${cerereId}/confirma-ridicare`, {
          method: 'POST',
          credentials: 'include'
        })
        const data = await res.json()
        if (res.ok && data.success) {
          // Reîncarcă detaliile elevului selectat
          await this.selecteazaElev(this.elevSelectat)
          // Reîncarcă și cererile globale
          await this.fetchBookRequests()
        } else {
          alert(data.message || 'Eroare la confirmare.')
        }
      } catch {
        alert('Eroare de rețea.')
      } finally {
        this.confirmandRidicare = null
      }
    },

    isOverdue(due_at) {
      if (!due_at) return false
      return new Date(due_at) < new Date()
    },
    deschideReturnareModal(b) {
      this.returnareTarget = b
      this.returnareNovaDataDate = b.due_at ? b.due_at.slice(0, 10) : ''
      this.returnareNovaDataTime = b.due_at ? b.due_at.slice(11, 16) : ''
      this.returnareMsg = { error: '', success: '' }
      this.returnareModalOpen = true
    },
    async prelungesteData() {
      if (!this.returnareNovaDataDate || !this.returnareNovaDataTime) return
      this.salvandData = true
      this.returnareMsg = { error: '', success: '' }
      const dataScadenta = `${this.returnareNovaDataDate}T${this.returnareNovaDataTime}`
      try {
        const res = await fetch(`/api/admin/loans/${this.returnareTarget.imprumut_id}/prelungeste`, {
          method: 'PUT',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ data_scadenta: dataScadenta })
        })
        const data = await res.json()
        if (res.ok && data.success) {
          this.returnareMsg.success = 'Data scadentă actualizată!'
          await this.selecteazaElev(this.elevSelectat)
        } else {
          this.returnareMsg.error = data.message || 'Eroare la actualizare.'
        }
      } catch {
        this.returnareMsg.error = 'Eroare de rețea.'
      } finally {
        this.salvandData = false
      }
    },
    async returneazaAcum() {
      this.procesandReturnare = true
      this.returnareMsg = { error: '', success: '' }
      try {
        const res = await fetch(`/api/admin/loans/${this.returnareTarget.imprumut_id}/returneaza`, {
          method: 'POST',
          credentials: 'include'
        })
        const data = await res.json()
        if (res.ok && data.success) {
          this.returnareMsg.success = 'Carte returnată cu succes!'
          await this.selecteazaElev(this.elevSelectat)
          setTimeout(() => { this.returnareModalOpen = false }, 1200)
        } else {
          this.returnareMsg.error = data.message || 'Eroare la returnare.'
        }
      } catch {
        this.returnareMsg.error = 'Eroare de rețea.'
      } finally {
        this.procesandReturnare = false
      }
    },

    // metode invitații club
    async generateInviteLink() {
      this.inviteLoading = true
      this.inviteError = ''
      this.generatedInviteLink = ''
      this.inviteCopied = false
      try {
        const res = await fetch('/api/club/invite', {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ expires_in_hours: this.inviteExpiry })
        })
        const data = await res.json()
        if (!res.ok || !data.success) {
          this.inviteError = data.message || 'Eroare la generarea link-ului.'
        } else {
          this.generatedInviteLink = window.location.origin + '/club/join/' + data.token
          this.inviteExpiresAt = data.expires_at
        }
      } catch {
        this.inviteError = 'Eroare de rețea. Încearcă din nou.'
      } finally {
        this.inviteLoading = false
      }
    },
    async fetchPendingThreads() {
      this.pendingThreadsLoading = true
      try {
        const res = await fetch('/api/club/threads/pending', { credentials: 'include' })
        const data = await res.json()
        if (res.ok) {
          this.pendingThreads = data.threads || []
        }
      } catch (err) { /* ignore */ } finally {
        this.pendingThreadsLoading = false
      }
    },
    async approveThread(threadId) {
      if (!confirm('Aprobați această discuție?')) return
      try {
        const res = await fetch(`/api/club/threads/${threadId}/approve`, { method: 'POST', credentials: 'include' })
        if (res.ok) {
          this.pendingThreads = this.pendingThreads.filter(t => t.thread_id !== threadId)
        }
      } catch (err) { /* ignore */ }
    },
    async rejectThread(threadId) {
      if (!confirm('Respingeți (ștergeți) această discuție?')) return
      try {
        const res = await fetch(`/api/club/threads/${threadId}`, { method: 'DELETE', credentials: 'include' })
        if (res.ok) {
          this.pendingThreads = this.pendingThreads.filter(t => t.thread_id !== threadId)
        }
      } catch (err) { /* ignore */ }
    },
    async copyInviteLink() {
      try {
        await navigator.clipboard.writeText(this.generatedInviteLink)
        this.inviteCopied = true
        setTimeout(() => { this.inviteCopied = false }, 2500)
      } catch {
        this.inviteError = 'Nu s-a putut copia. Copiază manual.'
      }
    }
  }
}
</script>

<style scoped>
</style>
