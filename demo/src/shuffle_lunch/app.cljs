(ns shuffle-lunch.app
  (:require [shuffle-lunch.data :refer [users cardinality total-pooled]]
            ["p5" :as p5]))


(def groups (partition cardinality users))
(def teams (distinct (map :team users)))

(def width 800)
(def height 800)
(def padding 6)
(def text-area-height 50)
(def size (- (/ height (max cardinality (count groups))) padding))

(defn team->hsb [t]
  (if (or (= t "(dummy)"))
    [0 0 0 0]
    [((zipmap teams (range 0 1 (/ 1 (count teams)))) t) 1 1]))

(defn setup []
  (js/createCanvas width (+ height text-area-height))
  (js/colorMode js/HSB))

(defn draw-group [users]
  (let [xs (map #(* % size) (range))
        r  (- size padding padding)]

    (js/fill 0 0 0 0.1)
    (js/stroke 0.5)
    (js/rect 0 0 size (* size (count users)))

    (js/push)
    (js/translate (/ size 2) (/ size 2))
    (doseq [[u y] (map vector users xs)
            :when (not (= (:team u) "(dummy)"))]
      (js/stroke 0.5)
      (apply js/fill (team->hsb (:team u)))
      (js/ellipse 0 y r r)

      (js/noStroke)
      (js/fill 1)
      (js/textAlign js/CENTER)
      (js/textSize 20)
      #_(js/text (:name u) 0 (+ y 7)))
    (js/pop))
  )

(defn draw []
  (js/colorMode js/HSB 1)
  (js/background 255)

  (js/push)
  (doseq [g groups]
    (draw-group g)
    (js/translate (+ size padding) 0))
  (js/pop)

  (js/textSize 35)
  (js/text (str "고인 정도: " total-pooled) padding (+ 50 (* cardinality size))))

(set! (.. js/window -setup) setup)
(set! (.. js/window -draw) draw)
