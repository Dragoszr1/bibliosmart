<template>
  <div id="app" class="min-h-screen">
    <!-- Hero Section -->
    <section class="bg-dark py-16 sm:py-24 relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-secondary/20 via-transparent to-accent/10"></div>
      <div class="max-w-3xl mx-auto px-6 text-center relative z-10">
        <h2 class="text-3xl sm:text-5xl font-bold text-white mb-3 tracking-tight">
          {{ isBibliotecar ? 'Panou Bibliotecar' : 'Profilul Meu' }}
        </h2>
        <p class="text-white/50 text-sm sm:text-lg font-normal">Bine ai revenit, {{ user.name }}</p>
      </div>
    </section>

    <!-- Main Content -->
    <main class="max-w-6xl mx-auto px-4 sm:px-6 py-10 sm:py-14">
      <!-- Top Row: Profile + Reviews side by side -->
      <div class="grid grid-cols-1 lg:grid-cols-5 gap-6 mb-6 sm:mb-8">
        <!-- Left: Profile Card -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-2xl shadow-card border border-gray-100 p-5 sm:p-6 h-full">
            <!-- Profile Picture -->
            <div class="flex flex-col items-center mb-4">
              <div class="relative group mb-3">
                <div class="w-24 sm:w-28 h-24 sm:h-28 rounded-full bg-cream shadow-card border-2 border-gray-100 overflow-hidden">
                  <img 
                    :src="user.profilePicture" 
                    :alt="user.name"
                    class="w-full h-full object-cover"
                    @error="user.profilePicture = 'https://api.dicebear.com/9.x/lorelei-neutral/svg?seed=default'"
                  >
                </div>
                <div 
                  @click="triggerFileInput"
                  class="absolute inset-0 flex items-center justify-center cursor-pointer"
                >
                  <div class="w-24 sm:w-28 h-24 sm:h-28 rounded-full bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center">
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
              <h1 class="text-lg sm:text-2xl font-bold text-dark">{{ user.name }}</h1>
              <!-- Role badge -->
              <span v-if="isBibliotecar" class="mt-1 px-3 py-0.5 bg-secondary text-white text-xs font-bold rounded-full">Bibliotecar</span>
              <p class="text-gray-500 text-xs mb-3 mt-1">Membru din {{ user.joinDate }}</p>
            </div>

            <!-- Description -->
            <div v-if="user.description" class="mb-4 px-1">
              <p class="text-gray-700 text-xs sm:text-sm leading-relaxed">{{ user.description }}</p>
            </div>
            <div v-else class="mb-4 px-1">
              <p class="text-gray-400 text-xs sm:text-sm italic">Nicio descriere încă.</p>
            </div>

            <!-- Stats -->
            <div class="flex items-center justify-center gap-4 py-3 border-t border-secondary/15">
              <div class="text-center">
                <p class="text-lg sm:text-xl font-bold text-secondary">{{ user.totalBooksRead }}</p>
                <p class="text-gray-500 text-xs">Cărți citite</p>
              </div>
              <div class="w-px h-8 bg-secondary/20"></div>
              <div class="text-center">
                <p class="text-lg sm:text-xl font-bold text-secondary">{{ user.userReviews.length }}</p>
                <p class="text-gray-500 text-xs">Recenzii</p>
              </div>
            </div>

            <!-- Edit Button -->
            <button @click="openProfileEditModal" class="btn-primary w-full mt-4 text-xs sm:text-sm">
              Editează Profil
            </button>
          </div>
        </div>

        <!-- Right: User Reviews -->
        <div class="lg:col-span-3">
          <div class="bg-white rounded-2xl shadow-card border border-gray-100 p-5 sm:p-6 h-full flex flex-col">
            <h2 class="text-lg sm:text-xl font-bold text-dark mb-4 flex items-center gap-2">
              <i class="pi pi-star text-secondary"></i> Recenziile Mele
            </h2>

            <!-- Loading -->
            <div v-if="loadingReviews" class="flex-1 flex items-center justify-center py-8">
              <i class="pi pi-spin pi-spinner text-2xl text-secondary"></i>
            </div>

            <!-- Empty state -->
            <div v-else-if="user.userReviews.length === 0" class="flex-1 flex flex-col items-center justify-center py-8">
              <i class="pi pi-comments text-3xl text-gray-300 mb-2"></i>
              <p class="text-gray-500 text-sm">Nicio recenzie încă</p>
            </div>

            <!-- Reviews list -->
            <div v-else class="flex-1 space-y-3 overflow-y-auto max-h-[400px] pr-1">
              <div v-for="review in user.userReviews" :key="review.id" class="bg-cream rounded-xl p-3 sm:p-4">
                <div class="flex items-start justify-between gap-2 mb-1">
                  <div class="min-w-0">
                    <h3 class="text-sm font-bold text-dark truncate">{{ review.titlu }}</h3>
                    <p class="text-gray-500 text-xs">de {{ review.autor }}</p>
                  </div>
                  <div class="flex items-center gap-0.5 flex-shrink-0">
                    <span v-for="star in 5" :key="star" :class="star <= review.nota ? 'text-accent' : 'text-gray-300'" class="text-sm">★</span>
                  </div>
                </div>
                <p class="text-gray-700 text-xs sm:text-sm leading-relaxed mt-2">{{ review.comentariu }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Books Read (regular users) -->
      <div v-if="!isBibliotecar">
        <h2 class="text-lg sm:text-xl font-bold text-dark mb-4 flex items-center gap-2">
          <i class="pi pi-book text-secondary"></i> Cărțile Citite
        </h2>

        <div v-if="user.booksRead.length === 0" class="bg-white rounded-2xl shadow-card border border-gray-100 p-8 sm:p-12 text-center">
          <i class="pi pi-book text-4xl sm:text-5xl text-secondary mb-4"></i>
          <p class="text-gray-600 text-sm sm:text-lg">Nici o carte citită</p>
        </div>

        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
          <div 
            v-for="(book, index) in user.booksRead" 
            :key="index"
            class="bg-white rounded-xl shadow-card border border-gray-100 p-3 sm:p-6 text-center hover:shadow-elevated transition-shadow"
          >
            <div class="mb-3 sm:mb-4 h-32 sm:h-40 rounded-lg bg-cream border border-gray-100 flex items-center justify-center">
              <i class="pi pi-book text-5xl sm:text-6xl text-secondary"></i>
            </div>
            <h3 class="text-sm sm:text-lg font-bold text-dark mb-1">{{ book.titlu }}</h3>
            <p class="text-gray-500 text-xs sm:text-sm mb-1">{{ book.autor }}</p>
            <p class="text-gray-600 text-xs">ISBN: {{ book.ISBN }}</p>
          </div>
        </div>
      </div>

      <!-- AI Recommendations (regular users only) -->
      <div v-if="!isBibliotecar" class="mt-4">
        <div class="bg-white rounded-2xl shadow-card border border-gray-100 p-5 sm:p-6">
          <div class="flex items-center justify-between gap-3 mb-4">
            <h2 class="text-lg sm:text-xl font-bold text-dark flex items-center gap-2">
              <i class="pi pi-sparkles text-secondary"></i> Recomandări AI
            </h2>
            <button
              @click="loadAiRecommendations"
              :disabled="loadingAi"
              class="px-4 py-2 bg-secondary hover:bg-secondary/90 text-white text-xs font-semibold rounded-lg transition-all disabled:opacity-50 flex items-center gap-2"
            >
              <i :class="loadingAi ? 'pi pi-spin pi-spinner' : 'pi pi-refresh'" class="text-xs"></i>
              {{ aiRecommendations ? 'Reîmprospătează' : 'Generează recomandări' }}
            </button>
          </div>

          <div v-if="!aiRecommendations && !loadingAi && !aiError" class="py-6 text-center">
            <i class="pi pi-sparkles text-4xl text-gray-300 mb-3"></i>
            <p class="text-gray-500 text-sm">Apasă butonul pentru a primi recomandări personalizate bazate pe cărțile tale.</p>
          </div>

          <div v-if="loadingAi" class="py-6 text-center">
            <i class="pi pi-spin pi-spinner text-2xl text-secondary mb-2"></i>
            <p class="text-gray-500 text-sm">Gemini analizează istoricul tău...</p>
          </div>

          <div v-if="aiError" class="py-4 text-center text-red-500 text-sm">
            <i class="pi pi-exclamation-triangle mr-2"></i>{{ aiError }}
          </div>

          <div v-if="aiRecommendations && !loadingAi" class="bg-cream rounded-xl p-4">
            <p class="text-dark text-sm leading-relaxed whitespace-pre-line">{{ aiRecommendations }}</p>
          </div>
        </div>
      </div>

      <!-- ═══════════════════════════════════════════════════════════ -->
      <!-- LIBRARIAN PANEL (only when rol='1') -->
      <!-- ═══════════════════════════════════════════════════════════ -->
      <div v-if="isBibliotecar" class="mt-2">

        <!-- ═══════════════════════════════════════════════════════════ -->
        <!-- BOOK REQUESTS (bibliotecar only) -->
        <!-- ═══════════════════════════════════════════════════════════ -->
        <div class="mb-8">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-6">
            <h2 class="text-lg sm:text-xl font-bold text-dark flex items-center gap-2">
              <i class="pi pi-inbox text-secondary"></i> Cereri Împrumut
              <span v-if="pendingRequestsCount > 0" class="ml-1 bg-accent text-white text-xs font-bold px-2 py-0.5 rounded-full">{{ pendingRequestsCount }}</span>
            </h2>
            <div class="flex gap-1.5">
              <button
                v-for="f in [{ key: 'all', label: 'Toate' }, { key: 'pending', label: 'În așteptare' }, { key: 'approved', label: 'Aprobate' }, { key: 'rejected', label: 'Respinse' }]"
                :key="f.key"
                @click="requestFilter = f.key; fetchBookRequests()"
                :class="[
                  'px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-150',
                  requestFilter === f.key
                    ? 'bg-secondary text-white'
                    : 'bg-white text-gray-500 border border-gray-200 hover:border-secondary/30 hover:text-secondary'
                ]"
              >
                {{ f.label }}
              </button>
            </div>
          </div>

          <!-- Loading -->
          <div v-if="loadingRequests" class="bg-white rounded-2xl shadow-card border border-gray-100 p-8 text-center">
            <i class="pi pi-spin pi-spinner text-2xl text-secondary"></i>
          </div>

          <!-- Empty -->
          <div v-else-if="bookRequests.length === 0" class="bg-white rounded-2xl shadow-card border border-gray-100 p-8 text-center">
            <i class="pi pi-inbox text-3xl text-gray-300 mb-2"></i>
            <p class="text-gray-500 text-sm">Nicio cerere {{ requestFilter !== 'all' ? 'cu acest status' : '' }}</p>
          </div>

          <!-- Requests List -->
          <div v-else class="space-y-3">
            <div
              v-for="req in bookRequests"
              :key="req.cerere_id"
              :class="[
                'bg-white rounded-xl shadow-card border overflow-hidden transition-all duration-150',
                req.status === 'pending' ? 'border-amber-200' : req.status === 'approved' ? 'border-green-200' : 'border-red-200'
              ]"
            >
              <div class="flex flex-col sm:flex-row sm:items-center gap-3 p-4">
                <!-- Info -->
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2 mb-1">
                    <span :class="[
                      'text-xs px-2 py-0.5 rounded-full font-medium',
                      req.status === 'pending' ? 'bg-amber-50 text-amber-700' :
                      req.status === 'approved' ? 'bg-green-50 text-green-700' :
                      'bg-red-50 text-red-700'
                    ]">
                      {{ req.status === 'pending' ? 'În așteptare' : req.status === 'approved' ? 'Aprobat' : 'Respins' }}
                    </span>
                    <span class="text-gray-400 text-xs">{{ formatDate(req.created_at) }}</span>
                  </div>
                  <p class="text-sm font-bold text-dark truncate">{{ req.titlu }}</p>
                  <p class="text-xs text-gray-500">de {{ req.autor }}</p>
                  <p class="text-xs text-gray-500 mt-1">
                    <i class="pi pi-user mr-1"></i>{{ req.username }}
                    <span class="ml-2 text-gray-400">({{ req.email }})</span>
                  </p>
                </div>

                <!-- Actions (only for pending) -->
                <div v-if="req.status === 'pending'" class="flex gap-2 flex-shrink-0">
                  <button
                    @click="openPickupModal(req)"
                    class="px-3 py-2 bg-green-600 hover:bg-green-700 text-white text-xs font-semibold rounded-lg transition-colors flex items-center gap-1"
                  >
                    <i class="pi pi-check text-xs"></i> Aprobă
                  </button>
                  <button
                    @click="handleRequest(req.cerere_id, 'rejected')"
                    class="px-3 py-2 bg-red-500 hover:bg-red-600 text-white text-xs font-semibold rounded-lg transition-colors flex items-center gap-1"
                  >
                    <i class="pi pi-times text-xs"></i> Respinge
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Section Header -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-6">
          <h2 class="text-lg sm:text-xl font-bold text-dark flex items-center gap-2">
            <i class="pi pi-cog text-secondary"></i> Gestionare Cărți
          </h2>
          <div class="flex gap-2">
            <button
              @click="downloadReport"
              :disabled="downloadingReport"
              class="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-60 text-white font-semibold rounded-lg text-xs sm:text-sm transition-all flex items-center gap-1"
              title="Descarcă raport Word cu toți elevii și împrumuturile lor"
            >
              <i :class="downloadingReport ? 'pi pi-spin pi-spinner' : 'pi pi-file-word'" class="mr-1"></i>
              Raport Word
            </button>
            <button @click="openAddBookModal" class="px-4 py-2 bg-secondary hover:bg-secondary/90 text-white font-semibold rounded-lg text-xs sm:text-sm transition-all">
              <i class="pi pi-plus mr-1"></i> Adaugă Carte
            </button>
          </div>
        </div>

        <!-- Search / Filter Bar -->
        <div class="bg-white rounded-2xl shadow-card border border-gray-100 p-4 mb-6">
          <div class="flex flex-col sm:flex-row gap-3">
            <div class="flex-1">
              <input
                v-model="libSearch"
                @input="filterLibBooks"
                type="text"
                placeholder="Caută carte după titlu, autor, ISBN..."
                class="input-field"
              >
            </div>
            <div class="text-sm text-gray-600 flex items-center">
              {{ filteredLibBooks.length }} cărți
            </div>
          </div>
        </div>

        <!-- Books Table -->
        <div class="bg-white rounded-2xl shadow-card border border-gray-100 overflow-hidden">
          <!-- Loading -->
          <div v-if="loadingBooks" class="flex items-center justify-center py-12">
            <i class="pi pi-spin pi-spinner text-2xl text-secondary"></i>
          </div>

          <!-- Table -->
          <div v-else class="overflow-x-auto">
            <table class="w-full text-left">
              <thead>
                <tr class="bg-dark text-cream text-xs sm:text-sm">
                  <th class="px-3 sm:px-4 py-3 font-semibold">Imagine</th>
                  <th class="px-3 sm:px-4 py-3 font-semibold">Titlu</th>
                  <th class="px-3 sm:px-4 py-3 font-semibold hidden sm:table-cell">Autor</th>
                  <th class="px-3 sm:px-4 py-3 font-semibold hidden md:table-cell">Gen</th>
                  <th class="px-3 sm:px-4 py-3 font-semibold hidden lg:table-cell">Poziție</th>
                  <th class="px-3 sm:px-4 py-3 font-semibold text-center">Stoc</th>
                  <th class="px-3 sm:px-4 py-3 font-semibold text-center">Disponibil</th>
                  <th class="px-3 sm:px-4 py-3 font-semibold text-center">Acțiuni</th>
                </tr>
              </thead>
              <tbody>
                <tr 
                  v-for="book in filteredLibBooks" 
                  :key="book.carte_id"
                  class="border-t border-gray-100 hover:bg-cream/50 transition-colors text-xs sm:text-sm"
                >
                  <!-- Image -->
                  <td class="px-3 sm:px-4 py-3">
                    <div class="w-12 h-16 rounded bg-cream border border-gray-100 overflow-hidden flex items-center justify-center relative group cursor-pointer" @click="triggerBookImageInput(book.carte_id)">
                      <img 
                        :src="'/api/books/image/' + book.carte_id + '?t=' + imageCacheBust" 
                        class="w-full h-full object-cover"
                        @error="$event.target.style.display='none'"
                      >
                      <i class="pi pi-image text-secondary/30 text-lg absolute" style="z-index: 0;"></i>
                      <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                        <i class="pi pi-camera text-white text-xs"></i>
                      </div>
                    </div>
                  </td>
                  <!-- Title -->
                  <td class="px-3 sm:px-4 py-3">
                    <p class="font-bold text-dark">{{ book.titlu }}</p>
                    <p class="text-gray-400 text-xs sm:hidden">{{ book.autor }}</p>
                    <p class="text-gray-400 text-xs">ISBN: {{ book.ISBN }}</p>
                  </td>
                  <!-- Author -->
                  <td class="px-3 sm:px-4 py-3 hidden sm:table-cell text-gray-700">{{ book.autor }}</td>
                  <!-- Genre -->
                  <td class="px-3 sm:px-4 py-3 hidden md:table-cell">
                    <span class="bg-cream text-secondary px-2 py-1 rounded-md text-xs font-medium">{{ book.gen }}</span>
                  </td>
                  <!-- Position -->
                  <td class="px-3 sm:px-4 py-3 hidden lg:table-cell text-gray-600 text-xs">{{ book.pozitie || '—' }}</td>
                  <!-- Stock Total -->
                  <td class="px-3 sm:px-4 py-3 text-center font-bold text-secondary">{{ book.stoc_total }}</td>
                  <!-- Stock Available -->
                  <td class="px-3 sm:px-4 py-3 text-center">
                    <span :class="book.stoc_disponibil > 0 ? 'text-green-600' : 'text-accent'" class="font-bold">{{ book.stoc_disponibil }}</span>
                  </td>
                  <!-- Actions -->
                  <td class="px-3 sm:px-4 py-3">
                    <div class="flex items-center justify-center gap-1">
                      <button @click="openEditBookModal(book)" class="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors" title="Editează">
                        <i class="pi pi-pencil text-sm"></i>
                      </button>
                      <button @click="openStockModal(book)" class="p-2 text-secondary hover:bg-secondary/10 rounded-lg transition-colors" title="Stoc">
                        <i class="pi pi-sort-alt text-sm"></i>
                      </button>
                      <button @click="confirmDeleteBook(book)" class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors" title="Șterge">
                        <i class="pi pi-trash text-sm"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>

            <!-- Empty -->
            <div v-if="filteredLibBooks.length === 0 && !loadingBooks" class="text-center py-12">
              <i class="pi pi-book text-3xl text-gray-300 mb-2"></i>
              <p class="text-gray-500 text-sm">Nicio carte găsită</p>
            </div>
          </div>
        </div>

        <!-- ═══════════════════════════════════════════════════════════ -->
        <!-- ANNOUNCEMENTS MANAGEMENT (bibliotecar only) -->
        <!-- ═══════════════════════════════════════════════════════════ -->
        <div class="mt-8">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-6">
            <h2 class="text-lg sm:text-xl font-bold text-dark flex items-center gap-2">
              <i class="pi pi-megaphone text-secondary"></i> Gestionare Anunțuri
            </h2>
            <button @click="openAddAnuntModal" class="px-4 py-2 bg-secondary hover:bg-secondary/90 text-white font-semibold rounded-lg text-xs sm:text-sm transition-all">
              <i class="pi pi-plus mr-1"></i> Anunț Nou
            </button>
          </div>

          <!-- Loading -->
          <div v-if="loadingAnunturi" class="bg-white rounded-2xl shadow-card border border-gray-100 p-8 text-center">
            <i class="pi pi-spin pi-spinner text-2xl text-secondary"></i>
          </div>

          <!-- Announcements list -->
          <div v-else class="space-y-4">
            <div 
              v-for="a in allAnunturi" 
              :key="a.anunt_id"
              class="bg-white rounded-xl shadow-card border border-gray-100 p-4 sm:p-6"
            >
              <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-2 mb-2">
                <div class="min-w-0 flex-1">
                  <h3 class="text-sm sm:text-lg font-bold text-dark">{{ a.titlu }}</h3>
                  <p class="text-gray-500 text-xs mt-1">
                    <i class="pi pi-calendar mr-1"></i>{{ a.data_publicare }}
                    <span class="ml-3"><i class="pi pi-thumbs-up mr-1"></i>{{ a.aprecieri }} aprecieri</span>
                  </p>
                </div>
                <div class="flex gap-1 flex-shrink-0">
                  <button @click="openEditAnuntModal(a)" class="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors" title="Editează">
                    <i class="pi pi-pencil text-sm"></i>
                  </button>
                  <button @click="confirmDeleteAnunt(a)" class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors" title="Șterge">
                    <i class="pi pi-trash text-sm"></i>
                  </button>
                </div>
              </div>
              <p class="text-gray-700 text-xs sm:text-sm leading-relaxed whitespace-pre-line">{{ a.anunt }}</p>
            </div>

            <!-- Empty -->
            <div v-if="allAnunturi.length === 0" class="bg-white rounded-2xl shadow-card border border-gray-100 p-8 text-center">
              <i class="pi pi-megaphone text-3xl text-gray-300 mb-2"></i>
              <p class="text-gray-500 text-sm">Niciun anunț încă</p>
            </div>
          </div>
        </div>

        <!-- ═══════════════════════════════════════════════════════════ -->
        <!-- USER ACCOUNTS (bibliotecar only) -->
        <!-- ═══════════════════════════════════════════════════════════ -->
        <div class="mt-8">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-6">
            <h2 class="text-lg sm:text-xl font-bold text-dark flex items-center gap-2">
              <i class="pi pi-users text-secondary"></i> Conturi Utilizatori
            </h2>
            <button @click="openUsersListModal" class="px-4 py-2 bg-secondary hover:bg-secondary/90 text-white font-semibold rounded-lg text-xs sm:text-sm transition-all">
              <i class="pi pi-list mr-1"></i> Vezi Toate Conturile
            </button>
          </div>
          <div class="bg-white rounded-2xl shadow-card border border-gray-100 p-6 text-center text-gray-400 text-sm">
            <i class="pi pi-users text-3xl mb-2 block text-gray-200"></i>
            Apasă butonul pentru a vizualiza și gestiona conturile elevilor.
          </div>
        </div>

      </div>
    </main>

    <!-- Hidden file input for book images -->
    <input ref="bookImageInput" type="file" accept="image/png,image/jpeg,image/jpg,image/gif,image/webp" class="hidden" @change="uploadBookImage">

    <!-- ═══════════ MODALS ═══════════ -->

    <!-- Pickup Interval Modal (approve book request) -->
    <div v-if="pickupModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm px-4" @click.self="pickupModalOpen = false">
      <div class="w-full max-w-md bg-white rounded-2xl shadow-modal p-6">
        <div class="flex items-center justify-between mb-5">
          <h2 class="text-lg font-bold text-dark flex items-center gap-2">
            <i class="pi pi-calendar-plus text-green-600"></i> Aprobă cerere
          </h2>
          <button @click="pickupModalOpen = false" class="text-gray-400 hover:text-secondary text-2xl font-bold leading-none">&times;</button>
        </div>

        <div class="bg-cream rounded-xl p-4 mb-5 border border-gray-100">
          <p class="text-sm font-bold text-dark truncate">{{ pickupReq.titlu }}</p>
          <p class="text-xs text-gray-500">de {{ pickupReq.autor }}</p>
          <p class="text-xs text-gray-500 mt-1">
            <i class="pi pi-user mr-1"></i>{{ pickupReq.username }}
            <span class="ml-2 text-gray-400">({{ pickupReq.email }})</span>
          </p>
        </div>

        <p class="text-sm text-gray-600 mb-4">Alege intervalul în care elevul poate ridica cartea. Un email de confirmare va fi trimis automat.</p>

        <div class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-gray-600 mb-1">De la (dată și oră)</label>
            <input
              v-model="pickupFrom"
              type="datetime-local"
              class="input-field"
            >
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-600 mb-1">Până la (dată și oră)</label>
            <input
              v-model="pickupUntil"
              type="datetime-local"
              class="input-field"
            >
          </div>
        </div>

        <p v-if="pickupError" class="text-xs text-red-500 mt-3">{{ pickupError }}</p>

        <div class="flex gap-3 mt-6">
          <button
            @click="pickupModalOpen = false"
            class="flex-1 px-4 py-2.5 border border-gray-200 text-gray-600 font-semibold rounded-xl text-sm hover:bg-gray-50 transition-colors"
          >
            Anulează
          </button>
          <button
            @click="confirmApprove"
            :disabled="approvingRequest"
            class="flex-1 px-4 py-2.5 bg-green-600 hover:bg-green-700 disabled:opacity-60 text-white font-semibold rounded-xl text-sm transition-colors flex items-center justify-center gap-2"
          >
            <i :class="approvingRequest ? 'pi pi-spin pi-spinner' : 'pi pi-check'" class="text-xs"></i>
            Aprobă și trimite email
          </button>
        </div>
      </div>
    </div>

    <!-- Edit Profile Modal -->
    <div v-if="editProfileOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm px-4" @click.self="editProfileOpen = false">
      <div class="w-full max-w-lg bg-white rounded-2xl shadow-modal p-6 sm:p-8">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-bold text-dark">Editează Profil</h2>
          <button @click="editProfileOpen = false" class="text-gray-500 hover:text-secondary text-2xl font-bold transition-colors duration-200">&times;</button>
        </div>
        <label class="block text-dark font-semibold mb-2 text-sm sm:text-base">Descriere</label>
        <textarea
          v-model="editDescription"
          rows="5"
          maxlength="255"
          placeholder="Scrie ceva despre tine..."
          class="input-field resize-none"
        ></textarea>
        <p class="text-gray-500 text-xs mt-1 text-right">{{ editDescription.length }} / 255</p>
        <div v-if="profileMsg.error" class="mt-3 bg-accent/10 border-l-4 border-accent rounded-lg p-3">
          <p class="text-accent text-xs sm:text-sm">{{ profileMsg.error }}</p>
        </div>
        <div v-if="profileMsg.success" class="mt-3 bg-green-50 border-l-4 border-green-500 rounded-lg p-3">
          <p class="text-green-700 text-xs sm:text-sm">{{ profileMsg.success }}</p>
        </div>
        <div class="mt-6 flex flex-col sm:flex-row gap-3">
          <button @click="saveDescription" :disabled="savingDescription" class="btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed">
            {{ savingDescription ? 'Se salvează...' : 'Modifică' }}
          </button>
          <button @click="editProfileOpen = false" class="btn-secondary flex-1">
            Anulează
          </button>
        </div>
      </div>
    </div>

    <!-- Add Book Modal -->
    <div v-if="addBookOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="addBookOpen = false">
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="addBookOpen = false"></div>
      <div class="relative bg-white rounded-2xl shadow-modal w-full max-w-lg z-10 p-6 sm:p-8 max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-bold text-dark">Adaugă Carte Nouă</h2>
          <button @click="addBookOpen = false" class="text-gray-500 hover:text-secondary text-2xl font-bold">&times;</button>
        </div>
        <form @submit.prevent="submitAddBook" class="space-y-4">
          <div>
            <label class="block text-dark font-semibold mb-1 text-sm">Titlu *</label>
            <input v-model="addForm.titlu" type="text" required class="input-field text-sm">
          </div>
          <div>
            <label class="block text-dark font-semibold mb-1 text-sm">Autor *</label>
            <input v-model="addForm.autor" type="text" required class="input-field text-sm">
          </div>
          <div>
            <label class="block text-dark font-semibold mb-1 text-sm">ISBN *</label>
            <input v-model="addForm.ISBN" type="text" required maxlength="13" class="input-field text-sm">
          </div>
          <div>
            <label class="block text-dark font-semibold mb-1 text-sm">Gen *</label>
            <input v-model="addForm.gen" type="text" required class="input-field text-sm">
          </div>
          <div>
            <label class="block text-dark font-semibold mb-1 text-sm">Poziție în bibliotecă</label>
            <input v-model="addForm.pozitie" type="text" placeholder="ex: Raft A3, Sala 2" class="input-field text-sm">
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-dark font-semibold mb-1 text-sm">Stoc Total</label>
              <input v-model.number="addForm.stoc_total" type="number" min="0" class="input-field text-sm">
            </div>
            <div>
              <label class="block text-dark font-semibold mb-1 text-sm">Stoc Disponibil</label>
              <input v-model.number="addForm.stoc_disponibil" type="number" min="0" class="input-field text-sm">
            </div>
          </div>
          <div v-if="addMsg.error" class="bg-accent/10 border-l-4 border-accent rounded-lg p-3">
            <p class="text-accent text-xs sm:text-sm">{{ addMsg.error }}</p>
          </div>
          <div v-if="addMsg.success" class="bg-green-50 border-l-4 border-green-500 rounded-lg p-3">
            <p class="text-green-700 text-xs sm:text-sm">{{ addMsg.success }}</p>
          </div>
          <button type="submit" class="w-full btn-primary">
            Adaugă Carte
          </button>
        </form>
      </div>
    </div>

    <!-- Edit Book Modal -->
    <div v-if="editBookOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="editBookOpen = false">
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="editBookOpen = false"></div>
      <div class="relative bg-white rounded-2xl shadow-modal w-full max-w-lg z-10 p-6 sm:p-8 max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-bold text-dark">Editează Carte</h2>
          <button @click="editBookOpen = false" class="text-gray-500 hover:text-secondary text-2xl font-bold">&times;</button>
        </div>
        <form @submit.prevent="submitEditBook" class="space-y-4">
          <div>
            <label class="block text-dark font-semibold mb-1 text-sm">Titlu</label>
            <input v-model="editBookForm.titlu" type="text" class="input-field text-sm">
          </div>
          <div>
            <label class="block text-dark font-semibold mb-1 text-sm">Autor</label>
            <input v-model="editBookForm.autor" type="text" class="input-field text-sm">
          </div>
          <div>
            <label class="block text-dark font-semibold mb-1 text-sm">ISBN</label>
            <input v-model="editBookForm.ISBN" type="text" maxlength="13" class="input-field text-sm">
          </div>
          <div>
            <label class="block text-dark font-semibold mb-1 text-sm">Gen</label>
            <input v-model="editBookForm.gen" type="text" class="input-field text-sm">
          </div>
          <div>
            <label class="block text-dark font-semibold mb-1 text-sm">Poziție în bibliotecă</label>
            <input v-model="editBookForm.pozitie" type="text" placeholder="ex: Raft A3, Sala 2" class="input-field text-sm">
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-dark font-semibold mb-1 text-sm">Stoc Total</label>
              <input v-model.number="editBookForm.stoc_total" type="number" min="0" class="input-field text-sm">
            </div>
            <div>
              <label class="block text-dark font-semibold mb-1 text-sm">Stoc Disponibil</label>
              <input v-model.number="editBookForm.stoc_disponibil" type="number" min="0" class="input-field text-sm">
            </div>
          </div>
          <div v-if="editBookMsg.error" class="bg-accent/10 border-l-4 border-accent rounded-lg p-3">
            <p class="text-accent text-xs sm:text-sm">{{ editBookMsg.error }}</p>
          </div>
          <div v-if="editBookMsg.success" class="bg-green-50 border-l-4 border-green-500 rounded-lg p-3">
            <p class="text-green-700 text-xs sm:text-sm">{{ editBookMsg.success }}</p>
          </div>
          <button type="submit" class="w-full btn-primary">
            Salvează Modificări
          </button>
        </form>
      </div>
    </div>

    <!-- Quick Stock Modal -->
    <div v-if="stockModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="stockModalOpen = false">
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="stockModalOpen = false"></div>
      <div class="relative bg-white rounded-2xl shadow-modal w-full max-w-sm z-10 p-6 sm:p-8">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-lg sm:text-xl font-bold text-secondary">Actualizare Stoc</h2>
          <button @click="stockModalOpen = false" class="text-gray-500 hover:text-secondary text-2xl font-bold">&times;</button>
        </div>
        <p class="text-dark font-semibold text-sm mb-4">{{ stockForm.titlu }}</p>
        <div class="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label class="block text-dark font-semibold mb-1 text-xs">Stoc Total</label>
            <input v-model.number="stockForm.stoc_total" type="number" min="0" class="input-field text-sm">
          </div>
          <div>
            <label class="block text-dark font-semibold mb-1 text-xs">Disponibil</label>
            <input v-model.number="stockForm.stoc_disponibil" type="number" min="0" class="input-field text-sm">
          </div>
        </div>
        <div v-if="stockMsg.error" class="mb-3 bg-accent/10 border-l-4 border-accent rounded-lg p-3">
          <p class="text-accent text-xs">{{ stockMsg.error }}</p>
        </div>
        <div v-if="stockMsg.success" class="mb-3 bg-green-50 border-l-4 border-green-500 rounded-lg p-3">
          <p class="text-green-700 text-xs">{{ stockMsg.success }}</p>
        </div>
        <button @click="submitStock" class="w-full btn-primary text-sm">
          Actualizează
        </button>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="deleteBookOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="deleteBookOpen = false">
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="deleteBookOpen = false"></div>
      <div class="relative bg-white rounded-2xl shadow-modal w-full max-w-md z-10 p-6 sm:p-8 text-center">
        <i class="pi pi-exclamation-triangle text-4xl text-accent mb-4"></i>
        <h2 class="text-xl font-bold text-dark mb-2">Șterge Cartea?</h2>
        <p class="text-gray-600 text-sm mb-6">
          Ești sigur că vrei să ștergi <strong>{{ deleteTarget?.titlu }}</strong>? Această acțiune nu poate fi anulată.
        </p>
        <div v-if="deleteMsg.error" class="mb-4 bg-accent/10 border-l-4 border-accent rounded-lg p-3">
          <p class="text-accent text-xs sm:text-sm">{{ deleteMsg.error }}</p>
        </div>
        <div class="flex gap-3">
          <button @click="deleteBookOpen = false" class="flex-1 btn-secondary">
            Anulează
          </button>
          <button @click="submitDeleteBook" class="flex-1 bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-lg transition-all duration-300">
            Șterge
          </button>
        </div>
      </div>
    </div>

    <!-- Add Announcement Modal -->
    <div v-if="addAnuntOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="addAnuntOpen = false">
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="addAnuntOpen = false"></div>
      <div class="relative bg-white rounded-2xl shadow-modal w-full max-w-lg z-10 p-6 sm:p-8 max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-bold text-dark">Anunț Nou</h2>
          <button @click="addAnuntOpen = false" class="text-gray-500 hover:text-secondary text-2xl font-bold">&times;</button>
        </div>
        <form @submit.prevent="submitAddAnunt" class="space-y-4">
          <div>
            <label class="block text-dark font-semibold mb-1 text-sm">Titlu *</label>
            <input v-model="addAnuntForm.titlu" type="text" required maxlength="255" class="input-field text-sm">
          </div>
          <div>
            <label class="block text-dark font-semibold mb-1 text-sm">Conținut *</label>
            <textarea v-model="addAnuntForm.anunt" required rows="6" class="input-field text-sm resize-none"></textarea>
          </div>
          <div v-if="addAnuntMsg.error" class="bg-accent/10 border-l-4 border-accent rounded-lg p-3">
            <p class="text-accent text-xs sm:text-sm">{{ addAnuntMsg.error }}</p>
          </div>
          <div v-if="addAnuntMsg.success" class="bg-green-50 border-l-4 border-green-500 rounded-lg p-3">
            <p class="text-green-700 text-xs sm:text-sm">{{ addAnuntMsg.success }}</p>
          </div>
          <button type="submit" class="w-full btn-primary">
            Publică Anunț
          </button>
        </form>
      </div>
    </div>

    <!-- Edit Announcement Modal -->
    <div v-if="editAnuntOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="editAnuntOpen = false">
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="editAnuntOpen = false"></div>
      <div class="relative bg-white rounded-2xl shadow-modal w-full max-w-lg z-10 p-6 sm:p-8 max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-bold text-dark">Editează Anunț</h2>
          <button @click="editAnuntOpen = false" class="text-gray-500 hover:text-secondary text-2xl font-bold">&times;</button>
        </div>
        <form @submit.prevent="submitEditAnunt" class="space-y-4">
          <div>
            <label class="block text-dark font-semibold mb-1 text-sm">Titlu</label>
            <input v-model="editAnuntForm.titlu" type="text" maxlength="255" class="input-field text-sm">
          </div>
          <div>
            <label class="block text-dark font-semibold mb-1 text-sm">Conținut</label>
            <textarea v-model="editAnuntForm.anunt" rows="6" class="input-field text-sm resize-none"></textarea>
          </div>
          <div v-if="editAnuntMsg.error" class="bg-accent/10 border-l-4 border-accent rounded-lg p-3">
            <p class="text-accent text-xs sm:text-sm">{{ editAnuntMsg.error }}</p>
          </div>
          <div v-if="editAnuntMsg.success" class="bg-green-50 border-l-4 border-green-500 rounded-lg p-3">
            <p class="text-green-700 text-xs sm:text-sm">{{ editAnuntMsg.success }}</p>
          </div>
          <button type="submit" class="w-full btn-primary">
            Salvează Modificări
          </button>
        </form>
      </div>
    </div>

    <!-- Delete Announcement Modal -->
    <div v-if="deleteAnuntOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="deleteAnuntOpen = false">
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="deleteAnuntOpen = false"></div>
      <div class="relative bg-white rounded-2xl shadow-modal w-full max-w-md z-10 p-6 sm:p-8 text-center">
        <i class="pi pi-exclamation-triangle text-4xl text-accent mb-4"></i>
        <h2 class="text-xl font-bold text-dark mb-2">Șterge Anunțul?</h2>
        <p class="text-gray-600 text-sm mb-6">
          Ești sigur că vrei să ștergi <strong>{{ deleteAnuntTarget?.titlu }}</strong>?
        </p>
        <div v-if="deleteAnuntMsg.error" class="mb-4 bg-accent/10 border-l-4 border-accent rounded-lg p-3">
          <p class="text-accent text-xs sm:text-sm">{{ deleteAnuntMsg.error }}</p>
        </div>
        <div class="flex gap-3">
          <button @click="deleteAnuntOpen = false" class="flex-1 btn-secondary">
            Anulează
          </button>
          <button @click="submitDeleteAnunt" class="flex-1 bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-lg transition-all duration-300">
            Șterge
          </button>
        </div>
      </div>
    </div>

    <!-- ═══════════ USERS LIST MODAL ═══════════ -->
    <div v-if="usersListOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="usersListOpen = false">
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="usersListOpen = false"></div>
      <div class="relative bg-white rounded-2xl shadow-modal w-full max-w-2xl z-10 flex flex-col max-h-[90vh]">
        <!-- Header -->
        <div class="flex items-center justify-between p-6 border-b border-gray-100">
          <h2 class="text-xl font-bold text-dark flex items-center gap-2">
            <i class="pi pi-users text-secondary"></i> Conturi Utilizatori
            <span class="text-sm font-normal text-gray-400 ml-1">({{ filteredUsers.length }})</span>
          </h2>
          <button @click="usersListOpen = false" class="text-gray-400 hover:text-secondary text-2xl font-bold transition-colors">&times;</button>
        </div>
        <!-- Search -->
        <div class="px-6 pt-4 pb-2">
          <input
            v-model="usersSearch"
            type="text"
            placeholder="Caută după nume sau email..."
            class="input-field text-sm"
          >
        </div>
        <!-- List -->
        <div class="overflow-y-auto flex-1 px-6 pb-6">
          <div v-if="loadingUsers" class="flex items-center justify-center py-12">
            <i class="pi pi-spin pi-spinner text-2xl text-secondary"></i>
          </div>
          <div v-else-if="filteredUsers.length === 0" class="text-center py-12 text-gray-400 text-sm">
            <i class="pi pi-users text-3xl mb-2 block text-gray-200"></i>
            Niciun utilizator găsit.
          </div>
          <div v-else class="space-y-2 mt-2">
            <div
              v-for="u in filteredUsers"
              :key="u.user_id"
              @click="openUserDetail(u)"
              class="flex items-center gap-4 p-3 rounded-xl border border-gray-100 hover:border-secondary/30 hover:bg-cream/50 cursor-pointer transition-all"
            >
              <div class="w-10 h-10 rounded-full bg-secondary/10 flex items-center justify-center flex-shrink-0">
                <i class="pi pi-user text-secondary"></i>
              </div>
              <div class="flex-1 min-w-0">
                <p class="font-semibold text-dark text-sm truncate">{{ u.username }}</p>
                <p class="text-gray-400 text-xs truncate">{{ u.email }}</p>
              </div>
              <span :class="u.rol === 'bibliotecar' ? 'bg-secondary text-white' : 'bg-cream text-secondary'" class="text-xs font-bold px-2 py-0.5 rounded-full flex-shrink-0">
                {{ u.rol === 'bibliotecar' ? 'Bibliotecar' : 'Elev' }}
              </span>
              <i class="pi pi-chevron-right text-gray-300 text-sm flex-shrink-0"></i>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ═══════════ USER DETAIL MODAL ═══════════ -->
    <div v-if="userDetailOpen" class="fixed inset-0 z-[60] flex items-center justify-center p-4" @click.self="userDetailOpen = false">
      <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="userDetailOpen = false"></div>
      <div class="relative bg-white rounded-2xl shadow-modal w-full max-w-2xl z-10 flex flex-col max-h-[90vh]">
        <!-- Header -->
        <div class="flex items-center justify-between p-6 border-b border-gray-100">
          <h2 class="text-xl font-bold text-dark flex items-center gap-2">
            <i class="pi pi-user text-secondary"></i>
            {{ userDetail ? userDetail.user.username : 'Detalii Cont' }}
          </h2>
          <button @click="userDetailOpen = false" class="text-gray-400 hover:text-secondary text-2xl font-bold transition-colors">&times;</button>
        </div>

        <!-- Loading -->
        <div v-if="loadingUserDetail" class="flex items-center justify-center py-16">
          <i class="pi pi-spin pi-spinner text-2xl text-secondary"></i>
        </div>

        <!-- Content -->
        <div v-else-if="userDetail" class="overflow-y-auto flex-1 p-6 space-y-6">

          <!-- Profile Info -->
          <div class="flex items-center gap-4 p-4 bg-cream rounded-xl">
            <img
              :src="`/api/auth/profile-picture/${encodeURIComponent(userDetail.user.username)}?t=${Date.now()}`"
              class="w-14 h-14 rounded-full object-cover border-2 border-white shadow"
              @error="$event.target.src='https://api.dicebear.com/7.x/avataaars/svg?seed=' + userDetail.user.username"
            >
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 flex-wrap">
                <p class="font-bold text-dark text-base">{{ userDetail.user.username }}</p>
                <span :class="userDetail.user.rol === 'bibliotecar' ? 'bg-secondary text-white' : 'bg-white text-secondary border border-secondary/20'" class="text-xs font-bold px-2 py-0.5 rounded-full">
                  {{ userDetail.user.rol === 'bibliotecar' ? 'Bibliotecar' : 'Elev' }}
                </span>
              </div>
              <p class="text-gray-500 text-sm">{{ userDetail.user.email }}</p>
              <p v-if="userDetail.user.telefon" class="text-gray-400 text-xs mt-0.5"><i class="pi pi-phone mr-1"></i>{{ userDetail.user.telefon }}</p>
            </div>
          </div>

          <p v-if="userDetail.user.description" class="text-gray-600 text-sm italic px-1">
            "{{ userDetail.user.description }}"
          </p>

          <!-- Stats row -->
          <div class="grid grid-cols-3 gap-3 text-center">
            <div class="bg-cream rounded-xl p-3">
              <p class="text-xl font-bold text-secondary">{{ userDetail.books_borrowed.length }}</p>
              <p class="text-gray-500 text-xs">Împrumutate</p>
            </div>
            <div class="bg-cream rounded-xl p-3">
              <p class="text-xl font-bold text-secondary">{{ userDetail.books_read.length }}</p>
              <p class="text-gray-500 text-xs">Citite</p>
            </div>
            <div class="bg-cream rounded-xl p-3">
              <p class="text-xl font-bold text-secondary">{{ userDetail.reviews.length }}</p>
              <p class="text-gray-500 text-xs">Recenzii</p>
            </div>
          </div>

          <!-- Currently Borrowed -->
          <div>
            <h3 class="text-sm font-bold text-dark mb-2 flex items-center gap-2">
              <i class="pi pi-book text-secondary"></i> Cărți Împrumutate Curent
            </h3>
            <div v-if="userDetail.books_borrowed.length === 0" class="text-gray-400 text-xs italic px-1">Nicio carte împrumutată momentan.</div>
            <div v-else class="space-y-2">
              <div v-for="b in userDetail.books_borrowed" :key="b.carte_id" class="flex items-center gap-3 p-3 border border-green-100 bg-green-50 rounded-xl">
                <i class="pi pi-book text-green-600 flex-shrink-0"></i>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-semibold text-dark truncate">{{ b.titlu }}</p>
                  <p class="text-xs text-gray-500">{{ b.autor }} · ISBN: {{ b.ISBN }}</p>
                </div>
                <span class="text-xs text-gray-400 flex-shrink-0">{{ formatDate(b.borrowed_at) }}</span>
              </div>
            </div>
          </div>

          <!-- Books Read -->
          <div>
            <h3 class="text-sm font-bold text-dark mb-2 flex items-center gap-2">
              <i class="pi pi-check-circle text-secondary"></i> Cărți Citite / Returnate
            </h3>
            <div v-if="userDetail.books_read.length === 0" class="text-gray-400 text-xs italic px-1">Nicio carte returnată înregistrată.</div>
            <div v-else class="space-y-2">
              <div v-for="b in userDetail.books_read" :key="b.carte_id" class="flex items-center gap-3 p-3 border border-gray-100 rounded-xl">
                <i class="pi pi-check text-secondary flex-shrink-0"></i>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-semibold text-dark truncate">{{ b.titlu }}</p>
                  <p class="text-xs text-gray-500">{{ b.autor }} · ISBN: {{ b.ISBN }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Borrow History -->
          <div>
            <h3 class="text-sm font-bold text-dark mb-2 flex items-center gap-2">
              <i class="pi pi-history text-secondary"></i> Istoric Cereri Împrumut
            </h3>
            <div v-if="userDetail.borrow_history.length === 0" class="text-gray-400 text-xs italic px-1">Nicio cerere înregistrată.</div>
            <div v-else class="space-y-2">
              <div v-for="r in userDetail.borrow_history" :key="r.cerere_id" class="flex items-center gap-3 p-3 border border-gray-100 rounded-xl">
                <span :class="[
                  'text-xs px-2 py-0.5 rounded-full font-medium flex-shrink-0',
                  r.status === 'pending' ? 'bg-amber-50 text-amber-700' :
                  r.status === 'approved' ? 'bg-green-50 text-green-700' :
                  'bg-red-50 text-red-700'
                ]">
                  {{ r.status === 'pending' ? 'Așteptare' : r.status === 'approved' ? 'Aprobat' : 'Respins' }}
                </span>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-semibold text-dark truncate">{{ r.titlu }}</p>
                  <p class="text-xs text-gray-500">{{ r.autor }}</p>
                </div>
                <span class="text-xs text-gray-400 flex-shrink-0">{{ formatDate(r.created_at) }}</span>
              </div>
            </div>
          </div>

          <!-- Reviews -->
          <div>
            <h3 class="text-sm font-bold text-dark mb-2 flex items-center gap-2">
              <i class="pi pi-star text-secondary"></i> Recenzii
            </h3>
            <div v-if="userDetail.reviews.length === 0" class="text-gray-400 text-xs italic px-1">Nicio recenzie scrisă.</div>
            <div v-else class="space-y-2">
              <div v-for="r in userDetail.reviews" :key="r.id" class="p-3 border border-gray-100 rounded-xl">
                <div class="flex items-center justify-between gap-2 mb-1">
                  <p class="text-sm font-semibold text-dark truncate">{{ r.titlu }}</p>
                  <div class="flex items-center gap-0.5 flex-shrink-0">
                    <span v-for="star in 5" :key="star" :class="star <= r.nota ? 'text-accent' : 'text-gray-200'" class="text-sm">★</span>
                  </div>
                </div>
                <p class="text-xs text-gray-500 mb-1">{{ r.autor }}</p>
                <p class="text-xs text-gray-700 leading-relaxed">{{ r.comentariu }}</p>
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
      // ── Profilul utilizatorului ──
      user: {
        name: '',
        profilePicture: 'https://api.dicebear.com/9.x/lorelei-neutral/svg?seed=default',
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
      // ── Panoul bibliotecarului ──
      bookRequests: [],
      loadingRequests: false,
      requestFilter: 'pending',
      downloadingReport: false,
      // Pickup interval modal
      pickupModalOpen: false,
      pickupReq: {},
      pickupFrom: '',
      pickupUntil: '',
      pickupError: '',
      approvingRequest: false,
      allBooks: [],
      filteredLibBooks: [],
      libSearch: '',
      loadingBooks: false,
      imageCacheBust: Date.now(),
      bookImageCarteId: null,
      // Add book
      addBookOpen: false,
      addForm: { titlu: '', autor: '', ISBN: '', gen: '', stoc_total: 1, stoc_disponibil: 1, pozitie: '' },
      addMsg: { error: '', success: '' },
      // Edit book
      editBookOpen: false,
      editBookForm: { carte_id: null, titlu: '', autor: '', ISBN: '', gen: '', stoc_total: 0, stoc_disponibil: 0, pozitie: '' },
      editBookMsg: { error: '', success: '' },
      // Stock quick-edit
      stockModalOpen: false,
      stockForm: { carte_id: null, titlu: '', stoc_total: 0, stoc_disponibil: 0 },
      stockMsg: { error: '', success: '' },
      // Delete book
      deleteBookOpen: false,
      deleteTarget: null,
      deleteMsg: { error: '' },
      // ── Anunțuri ──
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
      // ── Lista utilizatorilor (bibliotecar) ──
      usersListOpen: false,
      allUsers: [],
      loadingUsers: false,
      usersSearch: '',
      // User detail modal
      userDetailOpen: false,
      loadingUserDetail: false,
      userDetail: null
    }
  },
  computed: {
    pendingRequestsCount() {
      return this.bookRequests.filter(r => r.status === 'pending').length
    },
    filteredUsers() {
      if (!this.usersSearch.trim()) return this.allUsers
      const q = this.usersSearch.toLowerCase()
      return this.allUsers.filter(u =>
        u.username.toLowerCase().includes(q) ||
        u.email.toLowerCase().includes(q)
      )
    }
  },
  mounted() {
    this.loadProfile()
  },
  methods: {
    // ═══════════ METODE PROFIL ═══════════
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

    // ═══════════ METODE BIBLIOTECAR ═══════════

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

    // ── Recomandări AI ──
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

    // ── Cereri de împrumut ──
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
      this.pickupFrom = `${dateStr}T08:00`
      this.pickupUntil = `${dateStr}T14:00`
      this.pickupModalOpen = true
    },

    async confirmApprove() {
      this.pickupError = ''
      if (!this.pickupFrom || !this.pickupUntil) {
        this.pickupError = 'Completează ambele câmpuri.'
        return
      }
      if (this.pickupFrom >= this.pickupUntil) {
        this.pickupError = 'Data de start trebuie să fie înainte de data de final.'
        return
      }
      this.approvingRequest = true
      try {
        const fmt = iso => {
          const d = new Date(iso)
          return d.toLocaleString('ro-RO', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
        }
        const res = await fetch(`/api/book-requests/${this.pickupReq.cerere_id}`, {
          method: 'PUT',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            status: 'approved',
            pickup_from: fmt(this.pickupFrom),
            pickup_until: fmt(this.pickupUntil)
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

    // ── Cărți ──
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

    // ── Adăugare carte ──
    openAddBookModal() {
      this.addForm = { titlu: '', autor: '', ISBN: '', gen: '', stoc_total: 1, stoc_disponibil: 1, pozitie: '' }
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

    // ── Editare carte ──
    openEditBookModal(book) {
      this.editBookForm = {
        carte_id: book.carte_id,
        titlu: book.titlu,
        autor: book.autor,
        ISBN: book.ISBN,
        gen: book.gen,
        stoc_total: book.stoc_total,
        stoc_disponibil: book.stoc_disponibil,
        pozitie: book.pozitie || ''
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

    // ── Actualizare rapidă stoc ──
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

    // ── Ștergere carte ──
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

    // ── Încărcare copertă carte ──
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

    // ═══════════ METODE ANUNȚURI ═══════════
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

    // ── Adăugare anunț ──
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

    // ── Editare anunț ──
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

    // ── Ștergere anunț ──
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

    // ═══════════ METODE CONTURI UTILIZATORI ═══════════
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
    }
  }
}
</script>

<style scoped>
</style>
