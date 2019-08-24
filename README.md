# Fitness First Singapore Class Booker

1. Make sure your computer wakes up in time to run the CRON job!

<pre><code>sudo pmset repeat wakeorpoweron MTWRFSU 07:58:00
</code></pre>

2. Set the CRON job

<pre><code>59 7 * * * python /Users/yeejie.tang/Documents/GitHub/fitness-first-class-booker/book_ff_class.py
</code></pre>
