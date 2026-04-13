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
                    @error="user.profilePicture = 'https://api.dicebear.com/7.x/avataaars/svg?seed=Profile'"
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

      <!-- ═══════════════════════════════════════════════════════════ -->
      <!-- LIBRARIAN PANEL (only when rol='1') -->
      <!-- ═══════════════════════════════════════════════════════════ -->
      <div v-if="isBibliotecar" class="mt-2">
        <!-- Section Header -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-6">
          <h2 class="text-lg sm:text-xl font-bold text-dark flex items-center gap-2">
            <i class="pi pi-cog text-secondary"></i> Gestionare Cărți
          </h2>
          <div class="flex gap-2">
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
      </div>
    </main>

    <!-- Hidden file input for book images -->
    <input ref="bookImageInput" type="file" accept="image/png,image/jpeg,image/jpg,image/gif,image/webp" class="hidden" @change="uploadBookImage">

    <!-- ═══════════ MODALS ═══════════ -->

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
  </div>
</template>

<script>
export default {
  name: 'Profile',
  data() {
    return {
      // ── User profile ──
      user: {
        name: '',
        profilePicture: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Profile',
        joinDate: 'Ianuarie 2023',
        description: null,
        totalBooksRead: 0,
        booksRead: [],
        userReviews: []
      },
      isBibliotecar: false,
      loadingReviews: false,
      // Edit profile
      editProfileOpen: false,
      editDescription: '',
      profileMsg: { error: '', success: '' },
      savingDescription: false,
      // ── Librarian panel ──
      allBooks: [],
      filteredLibBooks: [],
      libSearch: '',
      loadingBooks: false,
      imageCacheBust: Date.now(),
      bookImageCarteId: null,
      // Add book
      addBookOpen: false,
      addForm: { titlu: '', autor: '', ISBN: '', gen: '', stoc_total: 1, stoc_disponibil: 1 },
      addMsg: { error: '', success: '' },
      // Edit book
      editBookOpen: false,
      editBookForm: { carte_id: null, titlu: '', autor: '', ISBN: '', gen: '', stoc_total: 0, stoc_disponibil: 0 },
      editBookMsg: { error: '', success: '' },
      // Stock quick-edit
      stockModalOpen: false,
      stockForm: { carte_id: null, titlu: '', stoc_total: 0, stoc_disponibil: 0 },
      stockMsg: { error: '', success: '' },
      // Delete book
      deleteBookOpen: false,
      deleteTarget: null,
      deleteMsg: { error: '' },
      // ── Announcements ──
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
      deleteAnuntMsg: { error: '' }
    }
  },
  mounted() {
    this.loadProfile()
  },
  methods: {
    // ═══════════ PROFILE METHODS ═══════════
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

        // Check role
        const meRes = await fetch('/api/auth/me', { credentials: 'include' })
        if (meRes.ok) {
          const me = await meRes.json()
          this.isBibliotecar = String(me.rol) === '1'
        }

        if (data.user_id) {
          this.loadBooksRead()
          this.loadUserReviews(data.user_id)
        }

        // Load librarian panel data
        if (this.isBibliotecar) {
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
    async loadUserReviews(userId) {
      this.loadingReviews = true
      try {
        const response = await fetch(`/api/reviews/user?user_id=${userId}`)
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

    // ═══════════ LIBRARIAN METHODS ═══════════
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

    // ── Add Book ──
    openAddBookModal() {
      this.addForm = { titlu: '', autor: '', ISBN: '', gen: '', stoc_total: 1, stoc_disponibil: 1 }
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

    // ── Edit Book ──
    openEditBookModal(book) {
      this.editBookForm = {
        carte_id: book.carte_id,
        titlu: book.titlu,
        autor: book.autor,
        ISBN: book.ISBN,
        gen: book.gen,
        stoc_total: book.stoc_total,
        stoc_disponibil: book.stoc_disponibil
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

    // ── Quick Stock Update ──
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

    // ── Delete Book ──
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

    // ── Book Image Upload ──
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

    // ═══════════ ANNOUNCEMENT METHODS ═══════════
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

    // ── Add Announcement ──
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

    // ── Edit Announcement ──
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

    // ── Delete Announcement ──
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
    }
  }
}
</script>

<style scoped>
</style>
