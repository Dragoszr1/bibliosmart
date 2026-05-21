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
                    @error="user.profilePicture = '/api/auth/profile-picture/default'"
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
      <!-- LIBRARIAN PANEL -->
      <!-- ═══════════════════════════════════════════════════════════ -->
      <div v-if="isBibliotecar" class="mt-2">

        <!-- Tab Bar -->
        <div class="flex gap-1 bg-white rounded-2xl shadow-card border border-gray-100 p-1.5 mb-6 overflow-x-auto">
          <button
            v-for="tab in [
              { key: 'cereri',   label: 'Cereri',   icon: 'pi pi-inbox' },
              { key: 'elevi',    label: 'Elevi',    icon: 'pi pi-users' },
              { key: 'anunturi', label: 'Anunțuri', icon: 'pi pi-megaphone' },
              { key: 'club',     label: 'Club',     icon: 'pi pi-bookmark' },
              { key: 'carti',    label: 'Cărți',    icon: 'pi pi-book' },
            ]"
            :key="tab.key"
            @click="activeTab = tab.key"
            :class="[
              'flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold transition-all duration-150 whitespace-nowrap flex-shrink-0',
              activeTab === tab.key
                ? 'bg-secondary text-white shadow-soft'
                : 'text-gray-500 hover:text-dark hover:bg-gray-50'
            ]"
          >
            <i :class="tab.icon" class="text-xs"></i>
            {{ tab.label }}
            <span v-if="tab.key === 'cereri' && pendingRequestsCount > 0" class="bg-white/30 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full">{{ pendingRequestsCount }}</span>
            <span v-if="tab.key === 'elevi' && approvedWaitingCount > 0" class="bg-amber-400 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full">{{ approvedWaitingCount }}</span>
          </button>
        </div>

        <!-- tab: cereri -->
        <div v-if="activeTab === 'cereri'" class="mb-8">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-6">
            <h2 class="text-lg sm:text-xl font-bold text-dark flex items-center gap-2">
              <i class="pi pi-inbox text-secondary"></i> Cereri Împrumut
              <span v-if="pendingRequestsCount > 0" class="ml-1 bg-accent text-white text-xs font-bold px-2 py-0.5 rounded-full">{{ pendingRequestsCount }}</span>
            </h2>
            <div class="flex gap-1.5">
              <button
                v-for="f in [{ key: 'all', label: 'Toate' }, { key: 'pending', label: 'În așteptare' }, { key: 'approved', label: 'Aprobate' }, { key: 'ridicat', label: 'Ridicate' }, { key: 'rejected', label: 'Respinse' }]"
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
                      req.status === 'pending'   ? 'bg-amber-50 text-amber-700' :
                      req.status === 'approved'  ? 'bg-blue-50 text-blue-700' :
                      req.status === 'ridicat' ? 'bg-green-50 text-green-700' :
                      'bg-red-50 text-red-700'
                    ]">
                      {{ { pending: 'În așteptare', approved: 'Aprobat', ridicat: 'Ridicat', rejected: 'Respins' }[req.status] || req.status }}
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

        </div><!-- end cereri tab -->

        <!-- tab: cărți -->
        <div v-if="activeTab === 'carti'">
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
                  <th class="px-3 sm:px-4 py-3 font-semibold text-center">PDF</th>
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
                  <!-- PDF -->
                  <td class="px-3 sm:px-4 py-3 text-center">
                    <div class="flex items-center justify-center gap-1">
                      <button v-if="book.has_pdf" @click="openPdfInTab(book.carte_id)" class="p-2 text-green-600 hover:bg-green-50 rounded-lg transition-colors" title="Vizualizează PDF">
                        <i class="pi pi-file-pdf text-sm"></i>
                      </button>
                      <button @click="triggerBookPdfInput(book.carte_id)" class="p-2 text-secondary hover:bg-secondary/10 rounded-lg transition-colors" :title="book.has_pdf ? 'Înlocuiește PDF' : 'Încarcă PDF'">
                        <i :class="book.has_pdf ? 'pi pi-refresh' : 'pi pi-upload'" class="text-sm"></i>
                      </button>
                      <button v-if="book.has_pdf" @click="deleteBookPdf(book)" class="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors" title="Șterge PDF">
                        <i class="pi pi-times text-sm"></i>
                      </button>
                    </div>
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

        </div><!-- end carti tab -->

        <!-- tab: anunțuri -->
        <div v-if="activeTab === 'anunturi'">
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
        </div><!-- end anunturi tab -->

        <!-- tab: elevi -->
        <div v-if="activeTab === 'elevi'">
          <h2 class="text-lg sm:text-xl font-bold text-dark flex items-center gap-2 mb-6">
            <i class="pi pi-users text-secondary"></i> Gestionare Elevi
          </h2>

          <!-- Two-column layout -->
          <div class="flex gap-4 min-h-[520px]">

            <!-- LEFT: user list -->
            <div class="w-60 flex-shrink-0 bg-white rounded-2xl shadow-card border border-gray-100 flex flex-col overflow-hidden">
              <div class="p-3 border-b border-gray-100">
                <input
                  v-model="eleviSearch"
                  type="text"
                  placeholder="Caută elev..."
                  class="w-full text-xs border border-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-secondary/40"
                />
              </div>
              <div class="flex-1 overflow-y-auto">
                <div v-if="loadingElevi" class="flex items-center justify-center py-8 text-gray-400">
                  <i class="pi pi-spin pi-spinner"></i>
                </div>
                <div v-else-if="eleviFiltrati.length === 0" class="text-center py-8 text-gray-400 text-xs px-3">
                  Niciun utilizator găsit.
                </div>
                <div
                  v-for="u in eleviFiltrati"
                  :key="u.user_id"
                  @click="selecteazaElev(u)"
                  :class="elevSelectat && elevSelectat.user_id === u.user_id
                    ? 'bg-secondary/10 border-l-4 border-secondary'
                    : 'hover:bg-gray-50 border-l-4 border-transparent'"
                  class="flex items-center gap-3 px-3 py-2.5 cursor-pointer transition-all"
                >
                  <div class="w-8 h-8 rounded-full bg-secondary/10 flex items-center justify-center flex-shrink-0 text-secondary text-xs font-bold uppercase">
                    {{ u.username.charAt(0) }}
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-semibold text-dark truncate">{{ u.username }}</p>
                    <p class="text-[11px] text-gray-400 truncate">{{ u.email }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- RIGHT: selected user detail -->
            <div class="flex-1 bg-white rounded-2xl shadow-card border border-gray-100 overflow-y-auto">

              <!-- Nothing selected -->
              <div v-if="!elevSelectat" class="flex flex-col items-center justify-center h-full text-gray-400 text-sm py-16">
                <i class="pi pi-arrow-left text-3xl mb-3 text-gray-200"></i>
                Selectează un elev din lista din stânga.
              </div>

              <!-- Loading detail -->
              <div v-else-if="loadingElevDetalii" class="flex items-center justify-center h-full py-16 text-gray-400">
                <i class="pi pi-spin pi-spinner text-2xl text-secondary"></i>
              </div>

              <!-- Detail content -->
              <div v-else-if="elevDetalii" class="p-6 space-y-6">

                <!-- Header user -->
                <div class="flex items-center gap-4 p-4 bg-cream rounded-xl">
                  <img
                    :src="`/api/auth/profile-picture/${encodeURIComponent(elevDetalii.user.username)}?t=${imageCacheBust}`"
                    class="w-14 h-14 rounded-full object-cover border-2 border-white shadow flex-shrink-0"
                    @error="$event.target.src='/api/auth/profile-picture/default'"
                  >
                  <div class="flex-1 min-w-0">
                    <p class="font-bold text-dark text-base">{{ elevDetalii.user.username }}</p>
                    <p class="text-gray-500 text-sm">{{ elevDetalii.user.email }}</p>
                    <p v-if="elevDetalii.user.telefon" class="text-gray-400 text-xs mt-0.5"><i class="pi pi-phone mr-1"></i>{{ elevDetalii.user.telefon }}</p>
                  </div>
                  <div class="flex-shrink-0 text-right">
                    <p class="text-xs text-gray-400">Ridicat: <span class="font-bold text-dark">{{ elevDetalii.books_borrowed.length }}</span></p>
                    <p class="text-xs text-gray-400">Citite: <span class="font-bold text-dark">{{ elevDetalii.books_read.length }}</span></p>
                  </div>
                </div>

                <!-- APROBATE — în așteptarea ridicării fizice -->
                <div>
                  <h3 class="text-sm font-bold text-dark mb-3 flex items-center gap-2">
                    <i class="pi pi-clock text-amber-500"></i> Aprobate — Așteptare ridicare fizică
                    <span v-if="aprovateAsteptare.length" class="bg-amber-100 text-amber-700 text-xs font-bold px-2 py-0.5 rounded-full">{{ aprovateAsteptare.length }}</span>
                  </h3>
                  <div v-if="aprovateAsteptare.length === 0" class="text-gray-400 text-xs italic">Nicio carte aprobată în așteptare.</div>
                  <div v-else class="space-y-2">
                    <div v-for="r in aprovateAsteptare" :key="r.cerere_id" class="flex items-center gap-3 p-3 border border-amber-200 bg-amber-50 rounded-xl">
                      <i class="pi pi-hourglass text-amber-500 flex-shrink-0"></i>
                      <div class="flex-1 min-w-0">
                        <p class="text-sm font-semibold text-dark truncate">{{ r.titlu }}</p>
                        <p class="text-xs text-gray-500">{{ r.autor }}</p>
                        <p v-if="r.ridicare_de_la" class="text-xs text-amber-700 mt-0.5">
                          <i class="pi pi-calendar mr-1"></i>{{ r.ridicare_de_la }} — {{ r.ridicare_pana_la }}
                        </p>
                      </div>
                      <button
                        @click="confirmaRidicare(r.cerere_id)"
                        :disabled="confirmandRidicare === r.cerere_id"
                        class="px-3 py-1.5 bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white font-semibold rounded-lg text-xs transition-all flex items-center gap-1 flex-shrink-0"
                      >
                        <i :class="confirmandRidicare === r.cerere_id ? 'pi pi-spin pi-spinner' : 'pi pi-check'" class="text-[10px]"></i>
                        Confirmă ridicarea
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Împrumutate activ (ridicate fizic) -->
                <div>
                  <h3 class="text-sm font-bold text-dark mb-3 flex items-center gap-2">
                    <i class="pi pi-book text-secondary"></i> Împrumutate curent (ridicate)
                  </h3>
                  <div v-if="elevDetalii.books_borrowed.length === 0" class="text-gray-400 text-xs italic">Nicio carte ridicată momentan.</div>
                  <div v-else class="space-y-2">
                    <div v-for="b in elevDetalii.books_borrowed" :key="b.imprumut_id" class="flex items-center gap-3 p-3 border border-green-100 bg-green-50 rounded-xl">
                      <i class="pi pi-book text-green-600 flex-shrink-0"></i>
                      <div class="flex-1 min-w-0">
                        <p class="text-sm font-semibold text-dark truncate">{{ b.titlu }}</p>
                        <p class="text-xs text-gray-500">{{ b.autor }}</p>
                        <p class="text-xs text-gray-400 mt-0.5">Ridicat: {{ formatDate(b.borrowed_at) }}</p>
                        <p class="text-xs text-red-400">Scadent: {{ formatDate(b.due_at) }}</p>
                      </div>
                      <button
                        @click="deschideReturnareModal(b)"
                        :class="isOverdue(b.due_at) ? 'bg-red-600 hover:bg-red-700' : 'bg-green-600 hover:bg-green-700'"
                        class="px-3 py-1.5 text-white font-semibold rounded-lg text-xs transition-all flex items-center gap-1 flex-shrink-0"
                      >
                        <i class="pi pi-undo text-[10px]"></i>
                        Returnează
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Returnate / citite -->
                <div>
                  <h3 class="text-sm font-bold text-dark mb-3 flex items-center gap-2">
                    <i class="pi pi-check-circle text-secondary"></i> Returnate / citite
                  </h3>
                  <div v-if="elevDetalii.books_read.length === 0" class="text-gray-400 text-xs italic">Nicio carte returnată.</div>
                  <div v-else class="space-y-2">
                    <div v-for="b in elevDetalii.books_read" :key="b.carte_id" class="flex items-center gap-3 p-3 border border-gray-100 rounded-xl">
                      <i class="pi pi-check text-secondary flex-shrink-0"></i>
                      <div class="flex-1 min-w-0">
                        <p class="text-sm font-semibold text-dark truncate">{{ b.titlu }}</p>
                        <p class="text-xs text-gray-500">{{ b.autor }}</p>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Istoricul complet cereri -->
                <div>
                  <h3 class="text-sm font-bold text-dark mb-3 flex items-center gap-2">
                    <i class="pi pi-history text-secondary"></i> Toate cererile
                  </h3>
                  <div v-if="elevDetalii.borrow_history.length === 0" class="text-gray-400 text-xs italic">Nicio cerere.</div>
                  <div v-else class="space-y-1.5">
                    <div v-for="r in elevDetalii.borrow_history" :key="r.cerere_id" class="flex items-center gap-3 p-2.5 border border-gray-100 rounded-xl">
                      <span :class="{
                        'bg-amber-50 text-amber-700': r.status === 'pending',
                        'bg-blue-50 text-blue-700':   r.status === 'approved',
                        'bg-green-50 text-green-700': r.status === 'ridicat',
                        'bg-red-50 text-red-700':     r.status === 'rejected'
                      }" class="text-[10px] px-2 py-0.5 rounded-full font-semibold flex-shrink-0">
                        {{ { pending: 'Așteptare', approved: 'Aprobat', ridicat: 'Ridicat', rejected: 'Respins' }[r.status] }}
                      </span>
                      <div class="flex-1 min-w-0">
                        <p class="text-xs font-semibold text-dark truncate">{{ r.titlu }}</p>
                        <p class="text-[10px] text-gray-400">{{ r.autor }}</p>
                      </div>
                      <span class="text-[10px] text-gray-400 flex-shrink-0">{{ formatDate(r.created_at) }}</span>
                    </div>
                  </div>
                </div>

              </div>
            </div>

          </div>
        </div><!-- end elevi tab -->

        <!-- tab: club -->
        <div v-if="activeTab === 'club'">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-6">
            <h2 class="text-lg sm:text-xl font-bold text-dark flex items-center gap-2">
              <i class="pi pi-bookmark text-secondary"></i> Invitații Club de Literatură
            </h2>
          </div>
          <div class="bg-white rounded-2xl shadow-card border border-gray-100 p-6">
            <p class="text-sm text-gray-500 mb-4">Generează un link de invitație pe care îl poți trimite elevilor. Link-ul îi va adăuga automat în clubul de literatură.</p>
            <div class="flex flex-wrap gap-3 mb-5">
              <label class="text-xs font-semibold text-gray-600 self-center">Valabilitate:</label>
              <button
                v-for="opt in inviteOptions"
                :key="opt.value"
                @click="inviteExpiry = opt.value"
                :class="inviteExpiry === opt.value
                  ? 'bg-secondary text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
                class="px-4 py-1.5 rounded-lg text-xs font-semibold transition-colors"
              >
                {{ opt.label }}
              </button>
            </div>
            <button
              @click="generateInviteLink"
              :disabled="inviteLoading"
              class="px-5 py-2.5 bg-secondary hover:bg-secondary/90 disabled:opacity-60 text-white font-semibold rounded-lg text-sm transition-all flex items-center gap-2"
            >
              <i :class="inviteLoading ? 'pi pi-spin pi-spinner' : 'pi pi-link'" class="text-xs"></i>
              Generează link
            </button>
            <div v-if="generatedInviteLink" class="mt-5">
              <label class="block text-xs font-semibold text-gray-600 mb-2">Link generat (expiră {{ inviteExpiresAt }}):</label>
              <div class="flex gap-2">
                <input
                  :value="generatedInviteLink"
                  readonly
                  class="input-field flex-1 text-xs font-mono bg-gray-50 cursor-text"
                />
                <button
                  @click="copyInviteLink"
                  class="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-dark font-semibold rounded-xl text-xs transition-colors flex items-center gap-1"
                >
                  <i :class="inviteCopied ? 'pi pi-check text-green-600' : 'pi pi-copy'"></i>
                  {{ inviteCopied ? 'Copiat!' : 'Copiază' }}
                </button>
              </div>
            </div>
            <div v-if="inviteError" class="mt-4 bg-accent/10 border-l-4 border-accent rounded-lg p-3">
              <p class="text-accent text-xs">{{ inviteError }}</p>
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
            <label class="block text-xs font-semibold text-gray-600 mb-1">De la</label>
            <div class="flex gap-2">
              <input v-model="pickupFromDate" type="date" class="input-field flex-1">
              <input
                v-model="pickupFromTime"
                type="text"
                placeholder="HH:MM"
                maxlength="5"
                @input="formatTimeInput('pickupFromTime', $event)"
                class="input-field w-28 font-mono"
              >
            </div>
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-600 mb-1">Până la</label>
            <div class="flex gap-2">
              <input v-model="pickupUntilDate" type="date" class="input-field flex-1">
              <input
                v-model="pickupUntilTime"
                type="text"
                placeholder="HH:MM"
                maxlength="5"
                @input="formatTimeInput('pickupUntilTime', $event)"
                class="input-field w-28 font-mono"
              >
            </div>
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
          <div>
            <label class="block text-dark font-semibold mb-1 text-sm">Cod</label>
            <input v-model="addForm.cod" type="text" placeholder="ex: BIO-042" class="input-field text-sm">
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
          <div>
            <label class="block text-dark font-semibold mb-1 text-sm">Cod</label>
            <input v-model="editBookForm.cod" type="text" placeholder="ex: BIO-042" class="input-field text-sm">
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

    <!-- RETURNARE ÎMPRUMUT MODAL -->
    <div v-if="returnareModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="returnareModalOpen = false">
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="returnareModalOpen = false"></div>
      <div class="relative bg-white rounded-2xl shadow-modal w-full max-w-sm z-10 p-6 sm:p-8">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-lg sm:text-xl font-bold text-secondary">Returnare Carte</h2>
          <button @click="returnareModalOpen = false" class="text-gray-500 hover:text-secondary text-2xl font-bold">&times;</button>
        </div>
        <p class="text-dark font-semibold text-sm mb-0.5">{{ returnareTarget?.titlu }}</p>
        <p class="text-gray-500 text-xs mb-5">{{ returnareTarget?.autor }}</p>

        <!-- Modificare dată scadentă -->
        <div class="mb-3">
          <label class="block text-dark font-semibold mb-1 text-xs">Modifică data scadentă</label>
          <div class="grid grid-cols-2 gap-2">
            <input v-model="returnareNovaDataDate" type="date" class="input-field text-sm">
            <input v-model="returnareNovaDataTime" type="time" class="input-field text-sm">
          </div>
        </div>
        <button
          @click="prelungesteData"
          :disabled="salvandData || !returnareNovaDataDate || !returnareNovaDataTime"
          class="w-full btn-secondary text-sm mb-5 disabled:opacity-50 flex items-center justify-center gap-1"
        >
          <i :class="salvandData ? 'pi pi-spin pi-spinner' : 'pi pi-calendar'"></i>
          {{ salvandData ? 'Se salvează...' : 'Salvează data scadentă' }}
        </button>

        <div class="border-t border-gray-100 mb-5"></div>

        <div v-if="returnareMsg.error" class="mb-3 bg-accent/10 border-l-4 border-accent rounded-lg p-3">
          <p class="text-accent text-xs">{{ returnareMsg.error }}</p>
        </div>
        <div v-if="returnareMsg.success" class="mb-3 bg-green-50 border-l-4 border-green-500 rounded-lg p-3">
          <p class="text-green-700 text-xs">{{ returnareMsg.success }}</p>
        </div>

        <button
          @click="returneazaAcum"
          :disabled="procesandReturnare"
          class="w-full btn-primary text-sm disabled:opacity-50 flex items-center justify-center gap-1"
        >
          <i :class="procesandReturnare ? 'pi pi-spin pi-spinner' : 'pi pi-check-circle'"></i>
          {{ procesandReturnare ? 'Se procesează...' : 'Returnează acum' }}
        </button>
      </div>
    </div>

    <!-- USERS LIST MODAL -->
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

    <!-- USER DETAIL MODAL -->
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
              @error="$event.target.src='/api/auth/profile-picture/default'"
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
      // Add book
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
