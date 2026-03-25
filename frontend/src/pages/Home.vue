<template>
  <div>
    <!-- Hero Section -->
    <section class="bg-gradient-to-b from-secondary to-dark py-8 sm:py-16 shadow-gold">
      <div class="max-w-full mx-auto px-3 sm:px-4 text-center">
        <h2 class="text-2xl sm:text-4xl font-bold text-gold mb-2 sm:mb-4 glow-gold">Bine venit la Biblioteca Școlii Tale</h2>
        <p class="text-primary text-xs sm:text-lg mb-4 sm:mb-8">Descoperi o lume de cunoștințe și posibilități infinite</p>
      </div>
    </section>

    <!-- Main Content -->
    <main class="max-w-full mx-auto px-3 sm:px-4 py-8 sm:py-12">
      <div class="flex flex-col lg:flex-row gap-6 lg:gap-8">
        <!-- Left Sidebar - Top Readers (Hidden on mobile) -->
        <aside class="hidden lg:block w-full lg:w-72 lg:flex-shrink-0">
          <div class="bg-gradient-to-b from-secondary to-dark rounded-lg shadow-dark-lg border-2 border-gold sticky top-24 p-4 sm:p-6 card-hover">
            <h3 class="text-lg sm:text-2xl font-bold text-gold mb-4 sm:mb-6 flex items-center gap-2 glow-gold">
<<<<<<< HEAD
              <i class="pi pi-trophy text-2xl sm:text-3xl"></i> Top Cititori
=======
              <i class="pi pi-trophy text-2xl sm:text-3xl text-gold"></i>
              Top Cititori
>>>>>>> c606094 (conectare db)
            </h3>
            <div class="space-y-3 sm:space-y-4">
              <div 
                v-for="(reader, index) in topReaders" 
                :key="index"
                class="bg-dark rounded-lg p-3 sm:p-4 border-l-4 border-gold card-hover shadow-gold text-sm"
              >
                <div class="flex items-center justify-between mb-2">
                  <h4 class="text-gold font-bold">{{ reader.name }}</h4>
                  <span class="text-primary text-xs font-semibold bg-secondary rounded-full px-2 py-1">{{ reader.rank }}</span>
                </div>
<<<<<<< HEAD
                <p class="text-white text-xs"><i class="pi pi-book text-gold mr-1"></i>{{ reader.booksRead }} cărți</p>
=======
                <p class="text-white text-xs">
                  <i class="pi pi-book text-gold mr-1"></i>
                  {{ reader.booksRead }} cărți
                </p>
>>>>>>> c606094 (conectare db)
                <div class="mt-2 bg-gold rounded-full h-2 overflow-hidden shadow-gold">
                  <div 
                    class="bg-primary h-full rounded-full transition-all duration-500" 
                    :style="{ width: reader.progress + '%' }"
                  ></div>
                </div>
              </div>
            </div>
            <button class="w-full mt-4 sm:mt-6 bg-gradient-to-r from-gold to-primary hover:shadow-gold text-dark font-bold py-2 sm:py-3 px-4 rounded-lg text-xs sm:text-base transition-all duration-300 transform hover:scale-105 btn-glow">
              Toți Cititorii
            </button>
          </div>
        </aside>

        <!-- Main Content - Announcements -->
        <section class="flex-1 min-w-0">
          <!-- Announcements Section -->
          <div class="bg-dark rounded-lg shadow-dark-lg border-2 border-gold p-4 sm:p-8 card-hover">
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6 sm:mb-8 gap-3">
              <h2 class="text-xl sm:text-3xl font-bold text-gold flex items-center gap-2 sm:gap-3 glow-gold">
<<<<<<< HEAD
                <i class="pi pi-megaphone text-2xl sm:text-4xl"></i> Anunțuri
=======
                <i class="pi pi-megaphone text-2xl sm:text-4xl text-gold"></i>
                Anunțuri
>>>>>>> c606094 (conectare db)
              </h2>
              <button class="w-full sm:w-auto bg-gradient-to-r from-gold to-primary hover:shadow-gold text-dark font-bold py-2 sm:py-3 px-4 sm:px-6 rounded-lg text-xs sm:text-base transition-all duration-300 transform hover:scale-105 btn-glow">
                + Anunț Nou
              </button>
            </div>

            <!-- Announcements List -->
            <div class="space-y-4 sm:space-y-6">
              <div 
                v-for="(announcement, index) in announcements" 
                :key="index"
                class="bg-gradient-to-b from-secondary to-dark rounded-lg p-4 sm:p-6 border-l-4 border-gold shadow-gold card-hover"
              >
                <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between mb-2 sm:mb-3 gap-2">
                  <div>
                    <h3 class="text-base sm:text-xl font-bold text-gold">{{ announcement.title }}</h3>
                    <p class="text-primary text-xs sm:text-sm mt-1">
                      De: <span class="font-semibold">{{ announcement.author }}</span> • {{ announcement.date }}
                    </p>
                  </div>
                  <span 
                    :class="[
                      'px-3 sm:px-4 py-1 sm:py-2 rounded-full text-xs font-semibold shadow-gold whitespace-nowrap',
                      announcement.category === 'Event' ? 'bg-accent text-white' :
                      announcement.category === 'Update' ? 'bg-gold text-dark' :
                      'bg-primary text-white'
                    ]"
                  >
                    {{ announcement.category }}
                  </span>
                </div>
                <p class="text-white mb-3 sm:mb-4 text-xs sm:text-base">{{ announcement.content }}</p>
                <div class="flex flex-wrap items-center gap-2 sm:gap-4 text-primary text-xs sm:text-sm">
<<<<<<< HEAD
                  <button class="hover:text-gold transition-colors duration-200 font-medium hover:scale-110 transform flex items-center gap-1"><i class="pi pi-thumbs-up"></i> Apreciază</button>
                  <button class="hover:text-gold transition-colors duration-200 font-medium hover:scale-110 transform flex items-center gap-1"><i class="pi pi-comments"></i> Comentează</button>
                  <button class="hover:text-gold transition-colors duration-200 font-medium hover:scale-110 transform flex items-center gap-1"><i class="pi pi-bookmark"></i> Salvează</button>
=======
                  <button class="hover:text-gold transition-colors duration-200 font-medium hover:scale-110 transform flex items-center gap-1">
                    <i class="pi pi-thumbs-up"></i>
                    Apreciază
                  </button>
                  <button class="hover:text-gold transition-colors duration-200 font-medium hover:scale-110 transform flex items-center gap-1">
                    <i class="pi pi-comments"></i>
                    Comentează
                  </button>
                  <button class="hover:text-gold transition-colors duration-200 font-medium hover:scale-110 transform flex items-center gap-1">
                    <i class="pi pi-bookmark"></i>
                    Salvează
                  </button>
>>>>>>> c606094 (conectare db)
                </div>
              </div>

              <!-- Empty State -->
              <div v-if="announcements.length === 0" class="text-center py-8 sm:py-12">
                <p class="text-white text-xs sm:text-lg">Nu sunt anunțuri deocamdată. Revino în curând!</p>
              </div>
            </div>
          </div>
        </section>

        <!-- Right Sidebar - Reserved for Future Use (Hidden on mobile) -->
        <aside class="hidden lg:block w-full lg:w-72 lg:flex-shrink-0">
          <div class="bg-gradient-to-b from-secondary to-dark rounded-lg shadow-dark-lg border-2 border-gold sticky top-24 p-4 sm:p-6 card-hover">
            <h3 class="text-lg sm:text-2xl font-bold text-gold mb-4 glow-gold">Curand</h3>
            <p class="text-white text-center py-6 sm:py-12 text-xs sm:text-base">
              Noi caracteristici și conțut vor fi adăugate aici curând!
            </p>
          </div>
        </aside>
      </div>

      <!-- Features Section -->
      <section class="bg-dark rounded-lg shadow-dark-lg p-4 sm:p-8 border-l-4 border-gold mt-8 sm:mt-12 card-hover">
        <h2 class="text-xl sm:text-3xl font-bold text-gold mb-4 sm:mb-6 glow-gold">De ce să Alegi Biblioteca?</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6 text-white">
          <div class="flex gap-3 sm:gap-4 p-3 sm:p-4 rounded-lg bg-secondary bg-opacity-50 border-l-2 border-gold shadow-gold card-hover">
            <span class="text-gold text-xl sm:text-2xl flex-shrink-0">✓</span>
            <div class="text-xs sm:text-base">
              <h4 class="font-bold text-gold mb-1">Colecție Vastă</h4>
              <p>Mii de cărți în toate genurile</p>
            </div>
          </div>
          <div class="flex gap-3 sm:gap-4 p-3 sm:p-4 rounded-lg bg-secondary bg-opacity-50 border-l-2 border-gold shadow-gold card-hover">
            <span class="text-gold text-xl sm:text-2xl flex-shrink-0">✓</span>
            <div class="text-xs sm:text-base">
              <h4 class="font-bold text-gold mb-1">Ghidare Expert</h4>
              <p>Bibliotecari gata să te ajute</p>
            </div>
          </div>
          <div class="flex gap-3 sm:gap-4 p-3 sm:p-4 rounded-lg bg-secondary bg-opacity-50 border-l-2 border-gold shadow-gold card-hover">
            <span class="text-gold text-xl sm:text-2xl flex-shrink-0">✓</span>
            <div class="text-xs sm:text-base">
              <h4 class="font-bold text-gold mb-1">Împrumut Ușor</h4>
              <p>Proces simplu de împrumut</p>
            </div>
          </div>
          <div class="flex gap-3 sm:gap-4 p-3 sm:p-4 rounded-lg bg-secondary bg-opacity-50 border-l-2 border-gold shadow-gold card-hover">
            <span class="text-gold text-xl sm:text-2xl flex-shrink-0">✓</span>
            <div class="text-xs sm:text-base">
              <h4 class="font-bold text-gold mb-1">Acces Digital</h4>
              <p>Cărți electronice și resurse</p>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>

export default {
  name: 'Home',
  data() {
    return {
      topReaders: [
        {
          name: 'Sarah Johnson',
          rank: '#1',
          booksRead: 24,
          progress: 95
        },
        {
          name: 'Michael Chen',
          rank: '#2',
          booksRead: 21,
          progress: 85
        },
        {
          name: 'Emma Wilson',
          rank: '#3',
          booksRead: 18,
          progress: 72
        },
        {
          name: 'David Martinez',
          rank: '#4',
          booksRead: 16,
          progress: 65
        },
        {
          name: 'Lisa Anderson',
          rank: '#5',
          booksRead: 14,
          progress: 58
        }
      ],
      announcements: [
        {
          title: 'Noua Colecție de Fiction Știintific Disponibilă',
          author: 'Asistent Bibliotecă',
          date: '20 martie 2026',
          category: 'Update',
          content: 'Suntem entuziasă să anunțăm adaugarea a 50 de romane noi de ficțiune știintifică la colecția noastră. De la autori clasici la lucrari contemporane, explorează lumi amazante și povești futuriste. Vizitează secțiunea Fiction Știintifică pentru mai multe detalii!'
        },
        {
          title: 'Baza anuală de Cărți - 5 aprilie',
          author: 'Administrator',
          date: '18 martie 2026',
          category: 'Event',
          content: 'Notează-ți în calendar! Baza anuală de cărți va avea loc pe 5 aprilie de la 9 AM la 6 PM. Întretiș-te cu autori locali, participă la concursuri de citire și bucură-te de reduceri exclusive la achiziț ionarea de cărți. Toți studenții și personalul sunt bine veniț!'
        },
        {
          title: 'Notificare de Íntreținere a Bibliotecii',
          author: 'Administrator',
          date: '15 martie 2026',
          category: 'Notice',
          content: 'Biblioteca va fi închisă pe 22 martie pentru íntreținere de sistem și actualizări. Îno s-a părut pentru orice inconvenient și ță mulțumim pentru răbdare. Biblioteca se va redeschide pe 23 martie.'
        }
      ]
    }
  }
}
</script>

<style scoped>
</style>
