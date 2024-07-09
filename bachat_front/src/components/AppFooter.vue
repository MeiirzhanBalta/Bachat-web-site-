<template>
  <div class="footer-wrapper">
    <div class="footer-container">
      <footer class="first-footer">
        <div class="footer-logo">
          <img src="../assets/logo.svg" alt="Logo">
        </div>
        <div class="social-container">
          <div class="footer-text">Our Social Networks</div>
          <div class="footer-links">
            <div class="footer-link">
              <img src="../assets/icons/icon_1.svg" alt="icon_1">
              <div>WhatsApp</div>
            </div>
            <div class="footer-link">
              <img src="../assets/icons/icon_2.svg" alt="icon_2">
              <div>Telegram</div>
            </div>
            <div class="footer-link">
              <img src="../assets/icons/icon_3.svg" alt="icon_3">
              <div>YouTube</div>
            </div>
          </div>
        </div>
      </footer>
      <footer class="second-footer">
        <div class="left-content">
          <div class="subscribe-section">
            <div class="subscribe-text">JOIN OUR TEAM</div>
            <form class="subscribe-form">
              <input type="email" placeholder="Enter your email address" required>
              <button type="submit">Subscribe</button>
            </form>
          </div>
        </div>
        <div class="right-content">
          <div class="info-column">
            <div class="info-heading">Service and Support</div>
            <ul class="info-list">
              <li>Support</li>
              <li>Instructions</li>
              <li>FAQs</li>
            </ul>
          </div>
          <div class="info-column" style="margin-left: 10px;">
            <div class="info-heading">Contacts</div>
            <ul class="info-list">
              <li>+371 26 209 984</li>
              <li>Weekdays from 09:00 to 18:00</li>
              <li>Address: Astana city</li>
            </ul>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AppFooter'
}
</script>


<style scoped>
@media (max-width: 1000px) {
  .footer-container {
    padding: 15px;
    /* Уменьшаем внешние отступы для маленьких экранов */
  }

  .first-footer,
  .second-footer {
    flex-direction: column;
    /* Стековое расположение элементов для маленьких экранов */
    padding: 15px;
  }

  .social-container,
  .right-content {
    justify-content: center;
    align-items: center;
  }

  .subscribe-form {
    flex-direction: column;
    /* Форма подписки теперь стековая на маленьких экранах */
  }

  .subscribe-form input,
  .subscribe-form button {
    max-width: 100%;
    max-height: 100%;
    /* Кнопка и инпут на всю ширину на маленьких экранах */
  }

  .info-heading,
  .footer-text,
  .footer-link div {
    font-size: 16px;
    /* Уменьшаем размер текста для читаемости */
  }

  .info-list li {
    font-size: 20;
    /* Делаем текст списка меньше на маленьких экранах */
  }
}
</style>
